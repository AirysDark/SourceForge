
import hashlib
from pathlib import Path
import json

OBJ_ROOT = Path("./objects")
OBJ_ROOT.mkdir(exist_ok=True)

def write_object(data: dict):
    raw = json.dumps(data).encode()
    sha = hashlib.sha1(raw).hexdigest()
    (OBJ_ROOT / sha).write_bytes(raw)
    return sha

def read_object(sha: str):
    p = OBJ_ROOT / sha
    if not p.exists():
        return None
    return json.loads(p.read_bytes())

def list_objects():
    return [p.name for p in OBJ_ROOT.iterdir() if p.is_file()]

def delete_object(sha: str):
    p = OBJ_ROOT / sha
    if p.exists():
        p.unlink()
