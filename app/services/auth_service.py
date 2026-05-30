from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password,verify_password,create_access_token,decode_token
from app.schemas.user import UserCreate
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_user(db : Session , user_data:UserCreate)->User:
    user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db : Session,username:str,password:str)->User | None:
    user=db.query(User).filter(User.username==username).first()
    if not user or not verify_password(password,user.hashed_password):
        return None
    return user

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload=decode_token(token)
        username=payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401,detail="Invalid Token")
    except:
        raise HTTPException(status_code=401,detail="Invalid Token")
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user