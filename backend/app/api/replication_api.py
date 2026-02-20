
from fastapi import APIRouter
from app.core.store import RefStore
from app.core.replication import Replicator

router = APIRouter()
store = RefStore()
replicator = Replicator()

def apply_event(event):
    if event["type"] == "ref_update":
        store.set_ref(event["repo"], event["ref"], event["sha"])

replicator.start_listener(apply_event)

@router.post("/ref/{repo}/{ref}")
def update_ref(repo: str, ref: str, data: dict):
    sha = data["sha"]
    store.set_ref(repo, ref, sha)

    replicator.publish({
        "type": "ref_update",
        "repo": repo,
        "ref": ref,
        "sha": sha
    })

    return {"replicated": True}

@router.get("/ref/{repo}/{ref}")
def read_ref(repo: str, ref: str):
    val = store.get_ref(repo, ref)
    if not val:
        return {"sha": None}
    return {"sha": val.decode()}
