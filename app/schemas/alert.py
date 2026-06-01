from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlertRuleCreate(BaseModel):
    app_id:int
    level:str
    threshold:int
    window_secs:int
    webhook_url:str
    
class AlertRuleUpdate(BaseModel):
    level:Optional[str]=None
    threshold:Optional[int]=None
    window_secs:Optional[int]=None
    webhook_url:Optional[str]=None

class AlertRuleOut(BaseModel):
    id:int
    app_id:int
    level:str
    threshold:int
    window_secs:int
    webhook_url:str
    created_at:datetime

    model_config={"from_attributes":True}