
from app.core.lock import DistributedLock
from app.git.refs.store import RefStore

lock_mgr = DistributedLock()
ref_store = RefStore()

def update_ref(repo, ref, new_sha):
    lock_key = f"lock:{repo}:{ref}"
    token = lock_mgr.acquire(lock_key)

    if not token:
        return False, "ref-locked"

    try:
        ref_store.set_ref(repo, ref, new_sha)
        return True, "updated"
    finally:
        lock_mgr.release(lock_key, token)
