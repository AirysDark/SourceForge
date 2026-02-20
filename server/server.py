import asyncio
import websockets
import json
import random
import time

async def handler(websocket):
    while True:
        await asyncio.sleep(5)
        msg_type = random.choice(["notification","queue"])
        if msg_type == "notification":
            data = {
                "type":"notification",
                "text": f"New review at {time.time():.0f}"
            }
        else:
            data = {
                "type":"queue",
                "item": {
                    "id": random.randint(20,99),
                    "title": "Auto-generated PR"
                }
            }
        await websocket.send(json.dumps(data))

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
