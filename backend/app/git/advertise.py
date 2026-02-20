# real-ish ref advertisement scaffold
from pathlib import Path
from app.git.pktline import pkt_line, pkt_flush

GIT_ROOT = Path("./repos")

CAPS = b"multi_ack side-band-64k thin-pack ofs-delta\0"

def list_refs(repo: str):
    ref_root = GIT_ROOT / repo / ".git" / "refs" / "heads"
    if not ref_root.exists():
        return []
    refs = []
    for f in ref_root.rglob("*"):
        if f.is_file():
            sha = f.read_text().strip()
            name = "refs/heads/" + f.relative_to(ref_root).as_posix()
            refs.append((sha, name))
    return refs

def advertise(repo: str):
    refs = list_refs(repo)
    if not refs:
        return pkt_flush()
    first_sha, first_ref = refs[0]
    out = pkt_line(first_sha.encode() + b" " + first_ref.encode() + b"\0" + CAPS)
    for sha, name in refs[1:]:
        out += pkt_line(sha.encode() + b" " + name.encode())
    out += pkt_flush()
    return out
