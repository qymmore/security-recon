import redis

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

def publish_update(channel, message):
    redis_client.publish(channel, message)