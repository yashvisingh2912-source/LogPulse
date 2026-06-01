from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,DateTime
from datetime import datetime,timezone
from sqlalchemy.orm import relationship
from app.database import Base

class AlertRule(Base):
    __tablename__ = "alert_rules"

    id=Column(Integer,primary_key=True,index=True)
    app_id=Column(Integer,ForeignKey("apps.id"),nullable=False)
    level=Column(String,nullable  = False)
    threshold=Column(Integer,nullable  = False)
    window_secs=Column(Integer,nullable  = False)
    webhook_url=Column(String,nullable  = False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

    app=relationship("App",back_populates="alert_rules")