import json
from pathlib import Path

ROOT = Path("./ci_status")
ROOT.mkdir(exist_ok=True)

def _file(repo, sha):
    return ROOT / f"{repo}_{sha}.json"

def set_status(repo, sha, context, state):
    p = _file(repo, sha)
    data = {}
    if p.exists():
        try: data = json.loads(p.read_text())
        except: data = {}
    data[context] = state
    p.write_text(json.dumps(data))

def get_statuses(repo, sha):
    p = _file(repo, sha)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except:
        return {}
