from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Text
from sqlalchemy.sql import func
from app.database import Base

class Log(Base):
    __tablename__="logs"

    id=Column(Integer,primary_key=True,index=True)
    app_id=Column(Integer,ForeignKey("apps.id"),nullable=False)
    level=Column(String,nullable=False,index=True)
    message=Column(Text,nullable=False)
    source=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),index=True)