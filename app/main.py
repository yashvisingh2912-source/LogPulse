from fastapi import FastAPI
from app.database import Base,engine
from app.routers import auth,logs,apps
from app.models import user,app,log

Base.metadata.create_all(bind=engine)

app_instance = FastAPI(title="LogPulse",version="1.0")

app_instance.include_router(auth.router)
app_instance.include_router(apps.router)
app_instance.include_router(logs.router)

@app_instance.get("/health")
def health():
    return {"Status":"ok"}