
import redis, json, hashlib
from app.config.settings import REDIS_URL, REGION_ID

class GitDAGCRDT:

    def __init__(self):
        self.client = redis.Redis.from_url(REDIS_URL)

    def _key(self, repo):
        return f"repo:{repo}:dag"

    def add_commit(self, repo, commit):
        # commit = { "sha": "...", "parents": [...] }
        raw = self.client.get(self._key(repo))
        if raw:
            dag = json.loads(raw)
        else:
            dag = { "commits": {}, "regions": {} }

        sha = commit["sha"]
        dag["commits"][sha] = commit

        # region counter (grow-only)
        dag["regions"][REGION_ID] = dag["regions"].get(REGION_ID, 0) + 1

        self.client.set(self._key(repo), json.dumps(dag))
        return dag

    def merge(self, repo, incoming_dag):
        raw = self.client.get(self._key(repo))
        if raw:
            current = json.loads(raw)
        else:
            current = { "commits": {}, "regions": {} }

        # grow-only merge of commits
        for sha, commit in incoming_dag["commits"].items():
            current["commits"][sha] = commit

        # grow-only merge of region counters
        for region, count in incoming_dag["regions"].items():
            current["regions"][region] = max(
                current["regions"].get(region, 0),
                count
            )

        self.client.set(self._key(repo), json.dumps(current))
        return current

    def get(self, repo):
        raw = self.client.get(self._key(repo))
        if not raw:
            return { "commits": {}, "regions": {} }
        return json.loads(raw)
