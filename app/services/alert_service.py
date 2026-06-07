from app.models.alert import AlertRule
from app.models.app import App
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.redis_client import get_redis_client
import httpx

async def evaluate_alert_rules():
    db:Session=SessionLocal()
    try:
        rules = db.query(AlertRule).filter(AlertRule.is_active==True).all()
        for rule in rules:
            key=f"logpulse:alerts:{rule.app_id}:{rule.level.upper()}:{rule.window_secs}"
            client=get_redis_client()
            count = await client.get(key)
            if count is None : 
                continue
            if int(count)>=rule.threshold:
                    await fire_webhook(rule,count)
                    await client.delete(key)
    finally:
         db.close()

async def fire_webhook(rule:AlertRule,count:int):
     payload={
          "alert_rule_id":rule.id,
          "app_id":rule.app_id,
          "level":rule.level,
          "threshold":rule.threshold,
          "window_secs":rule.window_secs,
          "current_count":count,
          "message":f"Alert triggered: {count} {rule.level} logs in {rule.window_secs}s (threshold: {rule.threshold})"
     }
     async with httpx.AsyncClient() as client:
          try:
               response=await client.post(rule.webhook_url,json=payload,timeout=5.0)
               print(f"Webhook fired for rule {rule.id} -> status {response.status_code}")
          except Exception as e:
               print(f"Webhook failed for rule {rule.id} -> {e}")

