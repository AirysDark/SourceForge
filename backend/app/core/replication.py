# backend/app/core/replication.py

import redis
import json
import threading
from app.config.settings import REDIS_URL, REGION_ID, DEBUG


class Replicator:

    def __init__(self):
        self.enabled = True

        try:
            self.client = redis.Redis.from_url(REDIS_URL)
            self.client.ping()  # test connection
            self.pubsub = self.client.pubsub()
            self.channel = "sf-replication"
        except Exception as e:
            print("[Replication] Redis unavailable — replication disabled")
            print(e)
            self.enabled = False
            self.client = None
            self.pubsub = None

    def publish(self, event):
        if not self.enabled:
            return

        payload = {
            "region": REGION_ID,
            "event": event
        }

        try:
            self.client.publish(self.channel, json.dumps(payload))
        except Exception as e:
            print("[Replication] Publish failed:", e)

    def start_listener(self, handler):
        if not self.enabled:
            return

        def run():
            try:
                self.pubsub.subscribe(self.channel)

                for msg in self.pubsub.listen():
                    if msg["type"] != "message":
                        continue

                    data = json.loads(msg["data"].decode())

                    if data["region"] == REGION_ID:
                        continue

                    handler(data["event"])

            except Exception as e:
                print("[Replication] Listener crashed:", e)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()