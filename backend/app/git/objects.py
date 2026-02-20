import hashlib
from pathlib import Path

GIT_ROOT = Path("./repos")

def object_path(repo: str, sha: str) -> Path:
    return GIT_ROOT / repo / ".git" / "objects" / sha[:2] / sha[2:]

def store_object(repo: str, data: bytes) -> str:
    sha = hashlib.sha1(data).hexdigest()
    path = object_path(repo, sha)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_bytes(data)
    return sha

def object_exists(repo: str, sha: str) -> bool:
    return object_path(repo, sha).exists()
