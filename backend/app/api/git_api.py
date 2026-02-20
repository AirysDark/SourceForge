
from fastapi import APIRouter
from app.core.git_crdt import GitDAGCRDT

router = APIRouter()
dag = GitDAGCRDT()

@router.post("/repo/{repo}/commit")
def add_commit(repo: str, data: dict):
    # expects: { "sha": "...", "parents": [...] }
    return dag.add_commit(repo, data)

@router.post("/repo/{repo}/merge")
def merge(repo: str, data: dict):
    # expects full incoming DAG structure
    return dag.merge(repo, data)

@router.get("/repo/{repo}/dag")
def get_dag(repo: str):
    return dag.get(repo)
