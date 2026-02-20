
import json
from pathlib import Path
from datetime import datetime

AUDIT_ROOT = Path("./audit_logs")
AUDIT_ROOT.mkdir(exist_ok=True)

def log_event(repo: str, event_type: str, payload: dict):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "repo": repo,
        "type": event_type,
        "payload": payload
    }
    file = AUDIT_ROOT / f"{repo}.log"
    with file.open("a") as f:
        f.write(json.dumps(entry) + "\n")

def read_events(repo: str):
    file = AUDIT_ROOT / f"{repo}.log"
    if not file.exists():
        return []
    with file.open() as f:
        return [json.loads(line) for line in f.readlines()]
