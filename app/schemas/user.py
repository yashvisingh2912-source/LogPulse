from pydantic import BaseModel

class UserCreate(BaseModel):
    username:str
    password:str

class UserOut(BaseModel):
    id:int
    username:str
    class Config:
        from_attribute=True

class Token(BaseModel):
    acess_token:str
    token_type:str