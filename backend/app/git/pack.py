import hashlib, struct
from pathlib import Path
from app.git.delta import make_delta

GIT_ROOT = Path("./repos")

def _collect_objects(repo: str):
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

def build_pack_with_deltas(repo: str):
    objs = _collect_objects(repo)

    header = b"PACK" + struct.pack(">II", 2, len(objs))
    body = b""

    prev_raw = None
    prev_offset = 0

    for sha, raw in objs:
        if prev_raw is not None:
            # pretend ofs-delta entry
            delta = make_delta(prev_raw, raw)
            obj_type = b'ofs-delta'
            entry = obj_type + delta
        else:
            entry = raw

        body += entry
        prev_raw = raw
        prev_offset += len(entry)

    pack = header + body
    checksum = hashlib.sha1(pack).digest()
    return pack + checksum
