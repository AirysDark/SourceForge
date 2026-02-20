
from fastapi import APIRouter
import hashlib, json
from app.git.storage.factory import get_storage

router = APIRouter()
storage = get_storage()

@router.post("/object/write")
def write(data: dict):
    raw = json.dumps(data).encode()
    sha = hashlib.sha1(raw).hexdigest()
    storage.write(sha, raw)
    return {"sha": sha}

@router.get("/object/read/{sha}")
def read(sha: str):
    raw = storage.read(sha)
    if not raw:
        return {"error": "not-found"}
    return json.loads(raw)

@router.get("/object/list")
def list_objects():
    return storage.list()

@router.delete("/object/delete/{sha}")
def delete(sha: str):
    storage.delete(sha)
    return {"deleted": sha}
