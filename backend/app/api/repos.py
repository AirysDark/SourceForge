from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import SessionLocal, PullRequest, MergeTrain

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- simulated helpers ---

def speculative_stack_ok(repo_id, pr_id, db):
    return True

def perform_rebase(pr):
    # simulated auto-rebase
    return True

# --- endpoints ---

@router.post("/repos/{repo_id}/train/enqueue")
def enqueue_train(repo_id:int, data:dict, db:Session=Depends(get_db)):
    pr = db.query(PullRequest).get(data["pr_id"])
    if not pr:
        raise HTTPException(status_code=404)

    pos = db.query(MergeTrain).filter_by(repo_id=repo_id).count()
    spec_ok = speculative_stack_ok(repo_id, pr.id, db)

    item = MergeTrain(
        repo_id=repo_id,
        pr_id=pr.id,
        position=pos,
        speculative_ok=spec_ok,
        needs_rebase=False
    )
    pr.status = "train"
    db.add(item)
    db.commit()
    return {"ok": True, "position": pos, "speculative": spec_ok}

@router.post("/repos/{repo_id}/train/rebuild")
def rebuild_train(repo_id:int, db:Session=Depends(get_db)):
    # mark downstream PRs for rebase
    items = (
        db.query(MergeTrain)
        .filter_by(repo_id=repo_id)
        .order_by(MergeTrain.position.asc())
        .all()
    )

    rebuilt = []
    for i, item in enumerate(items):
        if i == 0:
            continue  # head doesn't need rebase
        item.needs_rebase = True
        rebuilt.append(item.pr_id)

    db.commit()
    return {"ok": True, "marked_for_rebase": rebuilt}

@router.post("/repos/{repo_id}/train/process")
def process_train(repo_id:int, data:dict, db:Session=Depends(get_db)):
    limit = data.get("limit", 2)

    items = (
        db.query(MergeTrain)
        .filter_by(repo_id=repo_id)
        .order_by(MergeTrain.position.asc())
        .limit(limit)
        .all()
    )

    merged = []
    rebased = []

    for item in items:
        pr = db.query(PullRequest).get(item.pr_id)

        # 🔥 AUTO REBASE if needed
        if item.needs_rebase:
            pr.status = "rebasing"
            if perform_rebase(pr):
                item.needs_rebase = False
                rebased.append(pr.id)
            else:
                pr.status = "failed"
                db.delete(item)
                continue

        # re-check speculative
        if not item.speculative_ok:
            pr.status = "failed"
            db.delete(item)
            continue

        pr.status = "merged"
        merged.append(pr.id)
        db.delete(item)

    db.commit()
    return {"ok": True, "merged": merged, "rebased": rebased}
