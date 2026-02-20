
from app.git.storage.objects import list_objects, read_object, delete_object
from pathlib import Path
import json, hashlib, time

PACK_ROOT = Path("./packs")
PACK_ROOT.mkdir(exist_ok=True)

def compute_reachable(heads):
    reachable = set()
    stack = list(heads)

    while stack:
        sha = stack.pop()
        if sha in reachable:
            continue
        reachable.add(sha)
        obj = read_object(sha)
        if obj and "parents" in obj:
            stack.extend(obj["parents"])

    return reachable

def consolidate_pack(reachable):
    pack_data = {}
    for sha in reachable:
        obj = read_object(sha)
        if obj:
            pack_data[sha] = obj

    raw = json.dumps(pack_data).encode()
    pack_sha = hashlib.sha1(raw).hexdigest()
    pack_path = PACK_ROOT / f"{pack_sha}.pack"
    pack_path.write_bytes(raw)
    return pack_sha

def prune_unreachable(reachable):
    all_objects = list_objects()
    pruned = []
    for sha in all_objects:
        if sha not in reachable:
            delete_object(sha)
            pruned.append(sha)
    return pruned

def run_full_gc(heads):
    start = time.time()

    reachable = compute_reachable(heads)
    pack_sha = consolidate_pack(reachable)
    pruned = prune_unreachable(reachable)

    duration = time.time() - start

    return {
        "reachable_count": len(reachable),
        "pack_created": pack_sha,
        "pruned_objects": pruned,
        "gc_time_seconds": round(duration, 6)
    }
