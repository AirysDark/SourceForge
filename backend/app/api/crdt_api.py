
from fastapi import APIRouter
from app.core.store import CRDTStore
from app.core.crdt import LWWRefCRDT

router = APIRouter()
store = CRDTStore()

@router.post("/ref/{key}")
def update_ref(key: str, data: dict):
    clock = data.get("clock", {})
    clock = LWWRefCRDT.increment_clock(clock)

    payload = {
        "value": data["value"],
        "clock": clock
    }

    return store.update(key, payload)

@router.get("/ref/{key}")
def read_ref(key: str):
    return store.read(key)
