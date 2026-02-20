from fastapi import APIRouter, Request, Response
from app.git.receive import parse_push, apply_push, report
from app.git.policy.status_store import set_status

router = APIRouter()

@router.post("/git/{repo}/git-receive-pack")
async def receive_pack(repo: str, request: Request):
    body = await request.body()
    cmds = parse_push(body)
    results = apply_push(repo, cmds)
    return Response(content=report(results),
                    media_type="application/x-git-receive-pack-result")

@router.post("/ci/{repo}/{sha}")
def set_ci_status(repo: str, sha: str, data: dict):
    set_status(repo, sha, data["context"], data["state"])
    return {"ok": True}
