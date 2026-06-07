from fastapi import FastAPI
from app.database import Base,engine
from app.routers import auth,logs,apps,alerts
from app.models import user,app,log,alert
from app.core.scheduler import start_scheduler,stop_scheduler
from contextlib import asynccontextmanager

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app:FastAPI):
    start_scheduler()
    yield
    stop_scheduler()

app_instance = FastAPI(title="LogPulse",version="1.0",lifespan=lifespan)

app_instance.include_router(auth.router)
app_instance.include_router(apps.router)
app_instance.include_router(logs.router)
app_instance.include_router(alerts.router)

@app_instance.get("/health")
def health():
    return {"status": "ok"}