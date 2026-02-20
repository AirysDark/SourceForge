
from pathlib import Path
from .interface import ObjectStorageBackend

ROOT = Path("./objects")
ROOT.mkdir(exist_ok=True)

class LocalStorage(ObjectStorageBackend):
    def write(self, key: str, data: bytes):
        (ROOT / key).write_bytes(data)

    def read(self, key: str):
        p = ROOT / key
        if not p.exists():
            return None
        return p.read_bytes()

    def delete(self, key: str):
        p = ROOT / key
        if p.exists():
            p.unlink()

    def list(self):
        return [p.name for p in ROOT.iterdir() if p.is_file()]
