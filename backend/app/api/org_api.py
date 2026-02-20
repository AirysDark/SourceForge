
from fastapi import APIRouter
from app.git.codeowners.parser import match_owners

router = APIRouter()

@router.post("/resolve/{repo}")
def resolve(repo: str, data: dict):
    files = data.get("files", [])
    return {"reviewers": match_owners(repo, files)}
