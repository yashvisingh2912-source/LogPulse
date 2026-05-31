from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.app import AppCreate,AppOut
from app.database import get_db
from app.models.user import User
from app.models.app import App
from app.services.auth_service import get_current_user
import secrets

router = APIRouter(prefix="/app",tags=["app"])

@router.post("/",response_model=AppOut)
def register_app(
    app_data:AppCreate,
    db:Session=Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(App).filter(App.name==app_data.name).first()
    if existing :
        raise HTTPException(status_code=400 , detail="App name already exists")
    app = App(
        name=app_data.name,
        api_key=secrets.token_hex(32),
        owner_id=current_user.id
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@router.get("/",response_model=list[AppOut])
def list_apps(db:Session = Depends(get_db),
              current_user:User=Depends(get_current_user)):
    return db.query(App).filter(App.owner_id==current_user.id).all