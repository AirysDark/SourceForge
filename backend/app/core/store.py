# backend/app/core/store.py

import redis
import json
from app.config.settings import REDIS_URL
from app.core.crdt import LWWRefCRDT


# ============================================
# Base Redis Client
# ============================================

class _RedisBase:
    def __init__(self):
        self.client = redis.Redis.from_url(REDIS_URL)


# ============================================
# CRDT Store (Low-level)
# ============================================

class CRDTStore(_RedisBase):

    def update(self, key: str, value: dict):
        raw = self.client.get(key)

        if raw:
            current = json.loads(raw)
            merged = LWWRefCRDT.merge(current, value)
        else:
            merged = value

        self.client.set(key, json.dumps(merged))
        return merged

    def read(self, key: str):
        raw = self.client.get(key)
        if not raw:
            return None
        return json.loads(raw)


# ============================================
# Ref Store (Git refs abstraction)
# ============================================

class RefStore(_RedisBase):

    def _key(self, repo: str, ref: str):
        return f"repo:{repo}:ref:{ref}"

    def set_ref(self, repo: str, ref: str, value: dict):
        key = self._key(repo, ref)
        return CRDTStore().update(key, value)

    def get_ref(self, repo: str, ref: str):
        key = self._key(repo, ref)
        return CRDTStore().read(key)

    def list_refs(self, repo: str):
        pattern = f"repo:{repo}:ref:*"
        keys = self.client.keys(pattern)

        refs = []
        for k in keys:
            refs.append(k.decode().split(":")[-1])

        return refs


# ============================================
# Conflict Store (for merge conflicts)
# ============================================

class ConflictStore(_RedisBase):

    def _key(self, repo: str, conflict_id: str):
        return f"repo:{repo}:conflict:{conflict_id}"

    def save(self, repo: str, conflict_id: str, data: dict):
        key = self._key(repo, conflict_id)
        self.client.set(key, json.dumps(data))
        return True

    def get(self, repo: str, conflict_id: str):
        key = self._key(repo, conflict_id)
        raw = self.client.get(key)
        if not raw:
            return None
        return json.loads(raw)

    def list(self, repo: str):
        pattern = f"repo:{repo}:conflict:*"
        keys = self.client.keys(pattern)

        conflicts = []
        for k in keys:
            conflicts.append(k.decode().split(":")[-1])

        return conflicts

    def delete(self, repo: str, conflict_id: str):
        key = self._key(repo, conflict_id)
        self.client.delete(key)
        return True