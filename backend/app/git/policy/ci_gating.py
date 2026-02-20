from pathlib import Path
import json
from app.git.policy.status_store import get_statuses

POLICY_ROOT = Path("./branch_policies")

def load_policy(repo: str):
    p = POLICY_ROOT / f"{repo}.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except:
        return {}

def check_ci_requirements(repo: str, ref: str, new_sha: str):
    pol = load_policy(repo)
    branch = ref.split("refs/heads/")[-1]
    bp = pol.get("protected_branches", {}).get(branch)
    if not bp:
        return True, "no-policy"

    required = bp.get("required_status_checks", [])
    if not required:
        return True, "no-ci-required"

    statuses = get_statuses(repo, new_sha)
    missing = []
    failed = []

    for ctx in required:
        state = statuses.get(ctx)
        if state is None:
            missing.append(ctx)
        elif state != "success":
            failed.append(ctx)

    if missing:
        return False, f"missing status checks: {','.join(missing)}"
    if failed:
        return False, f"failing status checks: {','.join(failed)}"

    return True, "ci-ok"
