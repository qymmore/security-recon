import redis
import asyncio
import json

r = redis.Redis(host="redis", port=6379, db=0)

def publish_update(scan_id, message):
    r.publish(f"scan:{scan_id}", json.dumps(message))


async def subscribe(scan_id):
    pubsub = r.pubsub()
    pubsub.subscribe(f"scan:{scan_id}")

    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            yield message["data"].decode()
        await asyncio.sleep(0.1)