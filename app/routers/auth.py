from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,UserOut,Token
from app.database import get_db
from app.services.auth_service import create_user,authenticate_user
from app.core.security import create_access_token



router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",response_model=UserOut)
def register(user_data:UserCreate,db:Session = Depends(get_db)):
    return create_user(db,user_data)

@router.post("/login",response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends() , db:Session = Depends(get_db)):
    user = authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    token = create_access_token({"sub":user.username})
    return {"access_token":token , "token_type":"bearer"}