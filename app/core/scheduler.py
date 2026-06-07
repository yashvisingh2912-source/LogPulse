from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.alert_service import evaluate_alert_rules

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(evaluate_alert_rules,"interval",seconds=30)
    scheduler.start()
    print("Scheduler started — evaluating alerts every 30s")

def stop_scheduler():
    scheduler.shutdown()
    print("Scheduler stopped")