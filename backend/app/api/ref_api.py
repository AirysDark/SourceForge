
from fastapi import APIRouter
from app.git.refs.transaction import update_ref
from app.git.refs.store import RefStore

router = APIRouter()
store = RefStore()

@router.post("/ref/{repo}/{ref}")
def set_ref(repo: str, ref: str, data: dict):
    ok, msg = update_ref(repo, ref, data["sha"])
    return {"ok": ok, "message": msg}

@router.get("/ref/{repo}")
def list_refs(repo: str):
    return store.list_refs(repo)
