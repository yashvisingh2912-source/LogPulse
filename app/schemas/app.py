from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AppCreate(BaseModel):
    name:str

class AppOut(BaseModel):
    id:int
    api_key:str
    owner_id:int
    created_at:Optional[datetime]=None

    class Config:
        from_attribute=True
