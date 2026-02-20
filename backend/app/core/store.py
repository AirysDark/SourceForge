
import redis, json
from app.config.settings import REDIS_URL
from app.core.crdt import LWWRefCRDT

class CRDTStore:

    def __init__(self):
        self.client = redis.Redis.from_url(REDIS_URL)

    def update(self, key, value):
        raw = self.client.get(key)

        if raw:
            current = json.loads(raw)
            merged = LWWRefCRDT.merge(current, value)
        else:
            merged = value

        self.client.set(key, json.dumps(merged))
        return merged

    def read(self, key):
        raw = self.client.get(key)
        if not raw:
            return None
        return json.loads(raw)
