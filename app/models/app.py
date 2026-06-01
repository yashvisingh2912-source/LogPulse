from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class App(Base):
    __tablename__ = "apps"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False,index=True,unique=True)
    api_key=Column(String,nullable=False,unique=True,index=True)
    owner_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    created_At=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)

    alert_rules = relationship("AlertRule",back_populates="app")