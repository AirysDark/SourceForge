
import redis
import json
import threading
from app.config.settings import REDIS_URL, REGION_ID

class Replicator:
    def __init__(self):
        self.client = redis.Redis.from_url(REDIS_URL)
        self.pubsub = self.client.pubsub()
        self.channel = "sf-replication"

    def publish(self, event):
        payload = {
            "region": REGION_ID,
            "event": event
        }
        self.client.publish(self.channel, json.dumps(payload))

    def start_listener(self, handler):
        def run():
            self.pubsub.subscribe(self.channel)
            for msg in self.pubsub.listen():
                if msg["type"] != "message":
                    continue
                data = json.loads(msg["data"].decode())
                if data["region"] == REGION_ID:
                    continue  # ignore self events
                handler(data["event"])
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
