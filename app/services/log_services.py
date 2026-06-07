from app.core.redis_client import get_redis_client

async def increment_log_counter(app_id:int,level:str,window_secs:int):
    key = f"logpulse:alerts:{app_id}:{level.upper()}:{window_secs}"
    client = get_redis_client()
    async with client.pipeline() as pipe:
        pipe.incr(key)
        pipe.expire(key,window_secs,nx=True)
        await pipe.execute()