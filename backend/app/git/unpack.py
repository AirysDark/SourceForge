# Very simplified pack unpacker scaffold
# Real Git packs are complex — this extracts raw chunks only.

from app.git.objects import store_object

def unpack_pack(repo: str, pack: bytes):
    # Skip simple PACK header if present
    if pack.startswith(b"PACK"):
        pack = pack[12:-20]  # naive strip (header+checksum)
    stored = []
    # Naive split: treat remaining bytes as single object
    if pack:
        sha = store_object(repo, pack)
        stored.append(sha)
    return stored
