# Branch protection engine (scaffold)

from pathlib import Path
import json

POLICY_ROOT = Path("./branch_policies")

def load_policy(repo: str):
    p = POLICY_ROOT / f"{repo}.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except:
        return {}

def check_branch_policy(repo: str, ref: str, user: str | None = None):
    pol = load_policy(repo)
    branch = ref.split("refs/heads/")[-1]

    bp = pol.get("protected_branches", {}).get(branch)
    if not bp:
        return True, "no-policy"

    # Example rules
    if bp.get("block_push", False):
        return False, f"branch '{branch}' is protected"

    if bp.get("require_user") and user not in bp.get("allowed_users", []):
        return False, "user not allowed"

    return True, "ok"
