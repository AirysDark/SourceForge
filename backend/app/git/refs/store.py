
import redis
from app.config.settings import REDIS_URL

class RefStore:
    def __init__(self):
        self.client = redis.Redis.from_url(REDIS_URL)

    def get_ref(self, repo, ref):
        return self.client.get(f"{repo}:ref:{ref}")

    def set_ref(self, repo, ref, sha):
        self.client.set(f"{repo}:ref:{ref}", sha)

    def list_refs(self, repo):
        keys = self.client.keys(f"{repo}:ref:*")
        return [k.decode().split(":")[-1] for k in keys]
