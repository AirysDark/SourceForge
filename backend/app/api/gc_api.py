
from fastapi import APIRouter
from app.git.storage.objects import write_object, list_objects
from app.git.gc.gc_engine import run_full_gc

router = APIRouter()

@router.post("/object/write")
def write(data: dict):
    return {"sha": write_object(data)}

@router.get("/object/list")
def list_objs():
    return list_objects()

@router.post("/gc/full")
def gc_full(data: dict):
    heads = data.get("heads", [])
    return run_full_gc(heads)
