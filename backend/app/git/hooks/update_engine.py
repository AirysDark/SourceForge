from app.git.policy.ci_gating import check_ci_requirements

def run_update(repo: str, ref: str, old_sha: str, new_sha: str, user=None):
    ok, msg = check_ci_requirements(repo, ref, new_sha)
    if not ok:
        return False, msg
    return True, "ok"
