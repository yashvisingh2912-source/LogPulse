from fastapi import APIRouter,Depends,HTTPException,Header,Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.log import LogCreate,LogOut,LogListResponse
from app.database import get_db
from app.models.user import User
from app.models.app import App
from app.models.log import Log
from app.services.auth_service import get_current_user
from typing import Optional

router = APIRouter(prefix="/logs",tags=["logs"])

def get_app_by_api_key(x_api_key:str=Header(...),db:Session=Depends(get_db)):
    app = db.query(App).filter(App.api_key==x_api_key).first()
    if not app:
        raise HTTPException(status_code=401,detail="Invalid API Key")
    return app

@router.post("/",response_model=LogOut,status_code=201)
def ingest_log(
    log_data:LogCreate,
    app:App=Depends(get_app_by_api_key),
    db:Session=Depends(get_db)
):
    log = Log(
        app_id=app.id,
        level=log_data.level,
        message=log_data.message,
        source=log_data.source
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@router.get("/",response_model=LogListResponse)
def get_logs(
    app:App=Depends(get_app_by_api_key),
    db:Session=Depends(get_db),
    level:Optional[str]=Query(None),
    source:Optional[str]=Query(None),
    page:int = Query(1,ge=1),
    page_size:int = Query(20,ge=1,le=100)
):
    query = db.query(Log).filter(Log.app_id==app.id)
    if level:
        query = db.query(Log).filter(Log.level==level)
    if source:
        query = db.query(Log).filter(Log.level==source)
    total=query.count()
    logs = query.order_by(Log.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()
    return {
        "total":total,
        "page":page,
        "page_size":page_size,
        "logs":logs
    }