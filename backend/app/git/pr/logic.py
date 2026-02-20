
from app.core.audit import log_event

PR_STORE = {}

def create_pr(repo, pr_id, author):
    PR_STORE[(repo, pr_id)] = {
        "author": author,
        "approvals": set(),
        "merged": False
    }
    log_event(repo, "PR_CREATED", {"pr_id": pr_id, "author": author})
    return PR_STORE[(repo, pr_id)]

def approve(repo, pr_id, user):
    pr = PR_STORE.get((repo, pr_id))
    if not pr:
        return None
    pr["approvals"].add(user)
    log_event(repo, "PR_APPROVED", {"pr_id": pr_id, "user": user})
    return pr

def merge(repo, pr_id, user):
    pr = PR_STORE.get((repo, pr_id))
    if not pr:
        return False, "missing-pr"
    pr["merged"] = True
    log_event(repo, "PR_MERGED", {"pr_id": pr_id, "merged_by": user})
    return True, "merged"
