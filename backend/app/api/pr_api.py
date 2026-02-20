
from fastapi import APIRouter
from app.git.pr.logic import create_pr, approve, merge
from app.core.audit import read_events

router = APIRouter()

@router.post("/pr/{repo}/{pr_id}/create")
def pr_create(repo: str, pr_id: int, data: dict):
    return create_pr(repo, pr_id, data["author"])

@router.post("/pr/{repo}/{pr_id}/approve")
def pr_approve(repo: str, pr_id: int, data: dict):
    return approve(repo, pr_id, data["user"])

@router.post("/pr/{repo}/{pr_id}/merge")
def pr_merge(repo: str, pr_id: int, data: dict):
    ok, msg = merge(repo, pr_id, data["user"])
    return {"ok": ok, "message": msg}

@router.get("/audit/{repo}")
def get_audit(repo: str):
    return read_events(repo)
