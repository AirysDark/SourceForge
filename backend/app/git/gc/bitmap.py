
from pathlib import Path
import json

BITMAP_FILE = Path("./objects/bitmap_index.json")

def build_bitmap(reachable_set):
    bitmap = {obj: 1 for obj in reachable_set}
    BITMAP_FILE.write_text(json.dumps(bitmap))

def load_bitmap():
    if not BITMAP_FILE.exists():
        return {}
    return json.loads(BITMAP_FILE.read_text())

def is_reachable(obj_sha):
    bitmap = load_bitmap()
    return bitmap.get(obj_sha) == 1
