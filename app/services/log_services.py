from app.core.redis_client import get_redis_client
import json
from datetime import datetime

async def increment_log_counter(app_id:int,level:str,window_secs:int):
    key = f"logpulse:alerts:{app_id}:{level.upper()}:{window_secs}"
    client = get_redis_client()
    async with client.pipeline() as pipe:
        pipe.incr(key)
        pipe.expire(key,window_secs,nx=True)
        await pipe.execute()

async def publish_log(app_id:int,log_data:dict):
    redis = get_redis_client()
    channel = f"logpulse:logs:{app_id}"
    payload = {}
    for key,value in log_data.items():
        if isinstance(value,datetime):
            payload[key]=value.isoformat()
        else:
            payload[key]=value
    result = await redis.publish(channel,json.dumps(payload))
    print(f"DEBUG publish_log: channel={channel}, result={result}")