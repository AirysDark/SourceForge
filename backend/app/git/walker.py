# Very simplified reachability walk scaffold
from pathlib import Path

GIT_ROOT = Path("./repos")

def list_all_objects(repo: str):
    obj_root = GIT_ROOT / repo / ".git" / "objects"
    if not obj_root.exists():
        return []
    out = []
    for d in obj_root.iterdir():
        if len(d.name) != 2:
            continue
        for f in d.iterdir():
            sha = d.name + f.name
            out.append((sha, f.read_bytes()))
    return out

def reachable_objects(repo: str, wants: list[str], haves: list[str] | None = None):
    # Scaffold behavior:
    # include all objects not already in client 'haves'
    all_objs = list_all_objects(repo)
    have_set = set(haves or [])
    selected = []
    for sha, raw in all_objs:
        if sha not in have_set:
            selected.append((sha, raw))
    return selected
