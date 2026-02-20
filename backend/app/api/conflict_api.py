
from fastapi import APIRouter
from app.core.store import ConflictStore
from app.core.vector_clock import VectorClock
from app.config.settings import REGION_ID

router = APIRouter()
store = ConflictStore()

@router.post("/update/{key}")
def update(key: str, data: dict):
    clock = data.get("clock", {})
    clock = VectorClock.increment(clock, REGION_ID)

    payload = {
        "value": data["value"],
        "clock": clock
    }

    return store.update(key, payload)

@router.get("/read/{key}")
def read(key: str):
    return store.read(key)
