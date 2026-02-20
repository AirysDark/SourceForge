# Example pre-receive hook
# Reject pushes to protected branch

def pre_receive(commands):
    for old_sha, new_sha, ref in commands:
        if ref.endswith("/main"):
            return False, "main is protected (demo hook)"
    return True, "ok"
