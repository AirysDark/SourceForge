import json
from pathlib import Path

ROOT = Path("./prs")
ROOT.mkdir(exist_ok=True)

def _file(repo, pr_id):
    return ROOT / f"{repo}_{pr_id}.json"

def save_pr(repo, pr_id, data):
    _file(repo, pr_id).write_text(json.dumps(data))

def load_pr(repo, pr_id):
    p = _file(repo, pr_id)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except:
        return None
