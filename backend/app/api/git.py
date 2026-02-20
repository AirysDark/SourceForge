from fastapi import APIRouter
from app.git.store import (
    write_blob, write_tree, write_commit,
    update_ref, read_ref, ensure_repo
)

router = APIRouter()

@router.post("/git/{repo}/init")
def init_repo(repo: str):
    ensure_repo(repo)
    return {"ok": True}

@router.post("/git/{repo}/blob")
def create_blob(repo: str, data: dict):
    sha = write_blob(repo, data["content"].encode())
    return {"sha": sha}

@router.post("/git/{repo}/tree")
def create_tree(repo: str, data: dict):
    sha = write_tree(repo, data["entries"])
    return {"sha": sha}

@router.post("/git/{repo}/commit")
def create_commit(repo: str, data: dict):
    sha = write_commit(
        repo,
        data["tree"],
        data.get("parent"),
        data.get("message", "commit")
    )
    return {"sha": sha}

@router.post("/git/{repo}/ref")
def set_ref(repo: str, data: dict):
    update_ref(repo, data["ref"], data["sha"])
    return {"ok": True}

@router.get("/git/{repo}/ref/{ref}")
def get_ref(repo: str, ref: str):
    sha = read_ref(repo, ref)
    return {"sha": sha}
