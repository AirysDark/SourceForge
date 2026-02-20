import json
from pathlib import Path
from app.git.policy.status_store import get_statuses

POLICY_ROOT = Path("./branch_policies")

def load_policy(repo):
    p = POLICY_ROOT / f"{repo}.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except:
        return {}

def check_ci(repo, branch, sha):
    pol = load_policy(repo)
    bp = pol.get("protected_branches", {}).get(branch, {})
    required = bp.get("required_status_checks", [])
    if not required:
        return True, "no-ci-required"

    statuses = get_statuses(repo, sha)
    missing = [c for c in required if c not in statuses]
    failing = [c for c in required if statuses.get(c) != "success"]

    if missing:
        return False, "missing checks: " + ",".join(missing)
    if failing:
        return False, "failing checks: " + ",".join(failing)
    return True, "ci-ok"

def check_reviews(repo, branch, approvals):
    pol = load_policy(repo)
    bp = pol.get("protected_branches", {}).get(branch, {})
    required = bp.get("required_reviews", 0)
    if approvals < required:
        return False, f"requires {required} approvals"
    return True, "reviews-ok"
