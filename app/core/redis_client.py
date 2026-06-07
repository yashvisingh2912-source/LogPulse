import redis.asyncio as aioredis
from app.config import settings

_redis_client = None

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        _redis_client=aioredis.from_url(settings.REDIS_URL,decode_responses=True)
    return _redis_client