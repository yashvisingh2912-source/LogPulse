from fastapi import FastAPI,APIRouter,Depends,HTTPException
from app.schemas.alert import AlertRuleCreate,AlertRuleOut,AlertRuleUpdate
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import get_current_user
from app.models.alert import AlertRule
from typing import List

router = APIRouter(prefix="/alerts",tags=["alerts"])

@router.post("/",response_model=AlertRuleOut)
def create_alert_rule(rule:AlertRuleCreate,
                      db:Session=Depends(get_db),
                      current_user=Depends(get_current_user)):
    db_rule = AlertRule(**rule.model_dump())
    db_rule.level=db_rule.level.upper()
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.get("/",response_model=List[AlertRuleOut])
def get_alert_rules(db:Session=Depends(get_db),
                   current_user=Depends(get_current_user)):
    return db.query(AlertRule).all()

@router.get("/{rule_id}",response_model=AlertRuleOut)
def get_alert_rule(rule_id:int,
                   db:Session=Depends(get_db),
                   current_user=Depends(get_current_user)):
    rule = db.query(AlertRule).filter(AlertRule.id==rule_id).first()
    if not rule:
        raise HTTPException(status_code=404,detail="Alert rule not Found")
    return rule

@router.patch("/{rule_id}",response_model=AlertRuleOut)
def update_alert_rule(rule_id:int,
                      updates:AlertRuleUpdate,
                      db:Session=Depends(get_db),
                      current_user=Depends(get_current_user)):
    rule = db.query(AlertRule).filter(AlertRule.id==rule_id).first()
    if not rule:
        raise HTTPException(status_code=404,detail="Alert rule not Found")
    for field,value in updates.model_dump(exclude_unset=True).items():
        setattr(rule,field,value)
    db.commit()
    db.refresh(rule)
    return rule

@router.delete("/{rule_id}")
def delete_alert_rule(rule_id:int,
                      db:Session=Depends(get_db),
                      current_user=Depends(get_current_user)):
    rule = db.query(AlertRule).filter(AlertRule.id==rule_id).first()
    if not rule:
        raise HTTPException(status_code=404,detail="Alert rule not Found")
    db.delete(rule)
    db.commit()
    return {"message":"Alert rule deleted"}