# backend/app/api/repos.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.db import SessionLocal, PullRequest, MergeTrain

router = APIRouter(prefix="/repos", tags=["repos"])


# -----------------------------
# DB Dependency
# -----------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Basic Repo Endpoints
# -----------------------------

@router.get("")
def list_repos():
    return [
        {"id": 1, "name": "alpha-repo"},
        {"id": 2, "name": "engine-core"},
        {"id": 3, "name": "ui-system"},
    ]


@router.get("/{repo_id}")
def get_repo(repo_id: int):
    return {
        "id": repo_id,
        "name": f"repo-{repo_id}",
        "description": "Example repository",
    }


@router.get("/{repo_id}/tree")
def get_tree(repo_id: int, path: str = Query("/")):
    return {
        "repo_id": repo_id,
        "path": path,
        "entries": [
            {"type": "dir", "name": "src"},
            {"type": "dir", "name": "docs"},
            {"type": "file", "name": "README.md"},
        ],
    }


@router.get("/{repo_id}/blob")
def get_blob(repo_id: int, path: str = Query(...)):
    return {
        "repo_id": repo_id,
        "path": path,
        "content": f"// Mock file content for {path}\n\nconsole.log('Hello from repo {repo_id}');"
    }


# -----------------------------
# Merge Train
# -----------------------------

def speculative_stack_ok(repo_id: int, pr_id: int, db: Session):
    return True


def perform_rebase(pr: PullRequest):
    return True


@router.post("/{repo_id}/train/enqueue")
def enqueue_train(repo_id: int, data: dict, db: Session = Depends(get_db)):
    pr = db.get(PullRequest, data["pr_id"])
    if not pr:
        raise HTTPException(status_code=404)

    pos = db.query(MergeTrain).filter_by(repo_id=repo_id).count()

    item = MergeTrain(
        repo_id=repo_id,
        pr_id=pr.id,
        position=pos,
        speculative_ok=True,
        needs_rebase=False,
    )

    pr.status = "train"
    db.add(item)
    db.commit()

    return {"ok": True, "position": pos}