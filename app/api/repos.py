from fastapi import APIRouter

router = APIRouter()

# --- Mock data ---
REPOS = [
    {
        "id": "repo_1",
        "name": "SourceForge-Core",
        "visibility": "public",
        "lastUpdated": "2026-02-19T10:00:00Z",
    }
]

TREE = {
    "/": [
        {"type": "dir", "name": "src"},
        {"type": "file", "name": "README.md"},
        {"type": "file", "name": "index.html"},
    ]
}

BLOBS = {
    "/README.md": "# SourceForge\nBackend scaffold ready.",
    "/index.html": "<html><body>SourceForge</body></html>",
}


@router.get("/repos")
def list_repos():
    return REPOS


@router.get("/repos/{repo_id}")
def repo_meta(repo_id: str):
    return REPOS[0]


@router.get("/repos/{repo_id}/tree")
def repo_tree(repo_id: str, path: str = "/"):
    return {"path": path, "entries": TREE.get(path, [])}


@router.get("/repos/{repo_id}/blob")
def repo_blob(repo_id: str, path: str):
    return {
        "path": path,
        "content": BLOBS.get(path, ""),
        "encoding": "utf-8",
    }


@router.get("/repos/{repo_id}/commits")
def repo_commits(repo_id: str, limit: int = 50):
    return [
        {
            "sha": "a1b2c3",
            "message": "Initial commit",
            "author": "system",
            "date": "2026-02-19T09:00:00Z",
        }
    ]


@router.get("/repos/{repo_id}/commit/{sha}/diff")
def repo_diff(repo_id: str, sha: str):
    return {
        "files": [
            {
                "path": "README.md",
                "additions": 3,
                "deletions": 1,
                "patch": "@@ -1 +1 @@\n-Hello\n+Hello World",
            }
        ]
    }
