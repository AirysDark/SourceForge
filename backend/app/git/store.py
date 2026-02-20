# Minimal Git DAG: blobs, trees, commits
import hashlib
from pathlib import Path

GIT_ROOT = Path("./repos")

def ensure_repo(repo: str):
    repo_path = GIT_ROOT / repo / ".git"
    (repo_path / "objects").mkdir(parents=True, exist_ok=True)
    (repo_path / "refs" / "heads").mkdir(parents=True, exist_ok=True)
    return repo_path

def _hash_and_store(repo: str, raw: bytes):
    repo_path = ensure_repo(repo)
    sha = hashlib.sha1(raw).hexdigest()
    obj_dir = repo_path / "objects" / sha[:2]
    obj_dir.mkdir(parents=True, exist_ok=True)
    obj_file = obj_dir / sha[2:]
    if not obj_file.exists():
        obj_file.write_bytes(raw)
    return sha

def write_blob(repo: str, data: bytes):
    header = f"blob {len(data)}\0".encode()
    return _hash_and_store(repo, header + data)

def write_tree(repo: str, entries: list):
    body = b""
    for e in entries:
        line = f'{e["mode"]} {e["name"]}\0'.encode() + bytes.fromhex(e["sha"])
        body += line
    header = f"tree {len(body)}\0".encode()
    return _hash_and_store(repo, header + body)

def write_commit(repo: str, tree_sha: str, parent: str | None, message: str):
    lines = [f"tree {tree_sha}"]
    if parent:
        lines.append(f"parent {parent}")
    lines.append("author SourceForge <sf@example> 0 +0000")
    lines.append("committer SourceForge <sf@example> 0 +0000")
    lines.append("")
    lines.append(message)
    payload = "\n".join(lines).encode()
    header = f"commit {len(payload)}\0".encode()
    return _hash_and_store(repo, header + payload)

def update_ref(repo: str, ref: str, sha: str):
    repo_path = ensure_repo(repo)
    ref_path = repo_path / "refs" / "heads" / ref
    ref_path.parent.mkdir(parents=True, exist_ok=True)
    ref_path.write_text(sha + "\n")

def read_ref(repo: str, ref: str):
    repo_path = ensure_repo(repo)
    ref_path = repo_path / "refs" / "heads" / ref
    if not ref_path.exists():
        return None
    return ref_path.read_text().strip()
