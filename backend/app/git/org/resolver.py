# backend/app/git/org/resolver.py

import json
from pathlib import Path

TEAM_ROOT = Path("./teams")


# -----------------------------
# Load Organization File
# -----------------------------

def load_org(repo: str):
    p = TEAM_ROOT / f"{repo}.json"

    if not p.exists():
        return {}

    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


# -----------------------------
# Team Info
# -----------------------------

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


# -----------------------------
# 🔥 REQUIRED: Owner Resolver
# -----------------------------

def resolve_owner(repo: str, owner: str):
    """
    Resolves an owner into a permission object.
    Supports:
      - Direct user ownership
      - Team ownership via org file
    """

    org = load_org(repo)

    # If owner is a team inside org
    if owner in org:
        return {
            "type": "team",
            "owner": owner,
            "members": expand_team(owner, org),
            "quorum": get_quorum(owner, org)
        }

    # Otherwise treat as individual user
    return {
        "type": "user",
        "owner": owner,
        "members": [owner],
        "quorum": 1
    }