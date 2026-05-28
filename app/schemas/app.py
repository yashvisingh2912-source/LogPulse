from pydantic import BaseModel
from datetime import datetime

class AppCreate(BaseModel):
    name:str

class AppOut(BaseModel):
    id:int
    api_key:str
    owner_id:int
    created_at:datetime

    class Config:
        from_attribute=True
