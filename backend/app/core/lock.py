
import redis
import uuid
import time
from app.config.settings import REDIS_URL

class DistributedLock:
    def __init__(self):
        self.client = redis.Redis.from_url(REDIS_URL)

    def acquire(self, key, ttl=10):
        token = str(uuid.uuid4())
        acquired = self.client.set(key, token, nx=True, ex=ttl)
        if acquired:
            return token
        return None

    def release(self, key, token):
        current = self.client.get(key)
        if current and current.decode() == token:
            self.client.delete(key)
            return True
        return False
