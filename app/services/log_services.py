from app.core.redis_client import redis_client

async def increment_log_counter(app_id:int,level:str,window_secs:int):
    key = f"logpulse:alerts:{app_id}:{level.upper()}:{window_secs}"
    
    async with redis_client.pipeline() as pipe:
        pipe.incr(key)
        pipe.expire(key,window_secs,nx=True)
        await pipe.execute()