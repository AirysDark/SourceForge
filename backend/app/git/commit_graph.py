# Realistic commit ancestry walker (scaffold but correct structure)
import zlib
from pathlib import Path

GIT_ROOT = Path("./repos")

def _obj_path(repo: str, sha: str) -> Path:
    return GIT_ROOT / repo / ".git" / "objects" / sha[:2] / sha[2:]

def read_commit(repo: str, sha: str) -> bytes | None:
    p = _obj_path(repo, sha)
    if not p.exists():
        return None
    raw = p.read_bytes()
    try:
        return zlib.decompress(raw)
    except:
        return raw  # fallback for loose scaffold objects

def get_parents(repo: str, sha: str):
    data = read_commit(repo, sha)
    if not data:
        return []
    parents = []
    for line in data.splitlines():
        if line.startswith(b"parent "):
            parents.append(line.split()[1].decode())
    return parents

def is_ancestor(repo: str, ancestor: str, descendant: str, limit: int = 10000):
    # BFS walk of commit graph
    if ancestor == descendant:
        return True

    seen = set()
    queue = [descendant]

    steps = 0
    while queue and steps < limit:
        cur = queue.pop(0)
        if cur in seen:
            continue
        seen.add(cur)

        parents = get_parents(repo, cur)
        if ancestor in parents:
            return True
        queue.extend(parents)
        steps += 1

    return False

def fast_forward_ok(repo: str, old_sha: str | None, new_sha: str) -> bool:
    if old_sha is None:
        return True
    return is_ancestor(repo, old_sha, new_sha)
