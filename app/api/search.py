from fastapi import APIRouter

router = APIRouter()


@router.get("/search")
def search(q: str):
    return {
        "repos": [{"name": "SourceForge-Core"}],
        "code": [{"path": "README.md"}],
        "issues": [{"title": "Improve UI"}],
    }
