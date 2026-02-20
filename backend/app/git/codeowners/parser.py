
from pathlib import Path
import fnmatch
from app.git.org.resolver import load_org, resolve_owner

CO_ROOT = Path("./codeowners")

def load_codeowners(repo: str):
    p = CO_ROOT / repo / "CODEOWNERS"
    if not p.exists():
        return []
    rules = []
    order = 0
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2:
            rules.append({
                "pattern": parts[0],
                "owners": parts[1:],
                "order": order
            })
            order += 1
    return rules

def specificity_score(pattern: str):
    length_score = len(pattern)
    wildcard_penalty = pattern.count("*") * 10
    depth_bonus = pattern.count("/") * 5
    return length_score + depth_bonus - wildcard_penalty

def match_owners(repo: str, changed_files):
    rules = load_codeowners(repo)
    org = load_org(repo)
    matched_users = set()

    for path in changed_files:
        best_rule = None
        best_score = None

        for rule in rules:
            if fnmatch.fnmatch(path, rule["pattern"]):
                score = specificity_score(rule["pattern"])
                if best_rule is None or score > best_score or (
                    score == best_score and rule["order"] > best_rule["order"]
                ):
                    best_rule = rule
                    best_score = score

        if best_rule:
            for owner in best_rule["owners"]:
                matched_users |= resolve_owner(owner, org)

    return sorted(matched_users)
