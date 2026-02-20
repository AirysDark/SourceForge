
from fastapi import APIRouter, Request
import time
from app.core.metrics import track_request, track_latency, set_active_refs, metrics_endpoint

router = APIRouter()

REF_STORE = {}

@router.post("/ref/{repo}/{ref}")
async def set_ref(repo: str, ref: str, data: dict, request: Request):
    start = time.time()
    track_request(request.method, "/ref/update")
    REF_STORE[f"{repo}:{ref}"] = data["sha"]
    set_active_refs(len(REF_STORE))
    duration = time.time() - start
    track_latency("/ref/update", duration)
    return {"updated": True}

@router.get("/metrics")
def metrics():
    return metrics_endpoint()
