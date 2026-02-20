# Pre-receive hook engine scaffold
import importlib.util
from pathlib import Path

HOOK_ROOT = Path("./hooks")  # repo-level hooks directory

def load_hook(repo: str):
    hook_file = HOOK_ROOT / repo / "pre_receive.py"
    if not hook_file.exists():
        return None

    spec = importlib.util.spec_from_file_location("pre_receive_hook", hook_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run_pre_receive(repo: str, commands):
    '''
    commands: list of (old_sha, new_sha, ref)
    Hook must return (ok: bool, message: str)
    '''
    mod = load_hook(repo)
    if not mod or not hasattr(mod, "pre_receive"):
        return True, "no-hook"

    try:
        return mod.pre_receive(commands)
    except Exception as e:
        return False, f"hook-error: {e}"
