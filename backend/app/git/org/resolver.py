
import json
from pathlib import Path

TEAM_ROOT = Path("./teams")

def load_org(repo: str):
    p = TEAM_ROOT / f"{repo}.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except:
        return {}

def get_team_info(owner: str, org: dict):
    return org.get(owner)

def expand_team(owner: str, org: dict):
    info = get_team_info(owner, org)
    if not info:
        return []
    return info.get("members", [])

def get_quorum(owner: str, org: dict):
    info = get_team_info(owner, org)
    if not info:
        return 0
    return info.get("quorum", 1)
