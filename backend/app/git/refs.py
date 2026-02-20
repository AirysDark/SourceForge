from pathlib import Path
from app.git.commit_graph import fast_forward_ok

GIT_ROOT = Path("./repos")

def _ref_path(repo: str, branch: str) -> Path:
    return GIT_ROOT / repo / ".git" / "refs" / "heads" / branch

def _lock_path(repo: str, branch: str) -> Path:
    return _ref_path(repo, branch).with_suffix(".lock")

def read_ref(repo: str, branch: str) -> str | None:
    p = _ref_path(repo, branch)
    if p.exists():
        return p.read_text().strip()
    return None

def acquire_lock(repo: str, branch: str):
    lp = _lock_path(repo, branch)
    lp.parent.mkdir(parents=True, exist_ok=True)
    if lp.exists():
        raise RuntimeError("ref is locked")
    lp.write_text("lock")

def release_lock(repo: str, branch: str):
    lp = _lock_path(repo, branch)
    if lp.exists():
        lp.unlink()

def update_ref_safe(repo: str, branch: str, old_sha: str, new_sha: str):
    acquire_lock(repo, branch)
    try:
        current = read_ref(repo, branch)
        if not fast_forward_ok(repo, current, new_sha):
            return False, "non-fast-forward"

        path = _ref_path(repo, branch)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_sha + "\n")
        return True, "ok"
    finally:
        release_lock(repo, branch)
