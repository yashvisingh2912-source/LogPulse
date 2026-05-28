from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List

class LogCreate(BaseModel):
    level:str
    message:str
    source:Optional[str]=None

class LogOut(BaseModel):
    id:int
    app_id:int
    level:str
    message:str
    source:Optional[str]
    created_at:datetime

    class Config:
        from_attribute=True

class LogListResponse(BaseModel):
    total:int
    page:int
    page_size:int
    logs:List[LogOut]