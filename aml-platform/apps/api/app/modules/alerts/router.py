from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.entities import Alert
router=APIRouter(prefix="/api/v1/alerts",tags=["alerts"])
@router.get("")
def list_alerts(status:str|None=None,severity:str|None=None,db:Session=Depends(get_db)):
    q=select(Alert)
    if status:q=q.where(Alert.status==status)
    if severity:q=q.where(Alert.severity==severity)
    return list(db.scalars(q.order_by(Alert.created_at.desc()).limit(500)))
@router.get("/{alert_id}")
def get_alert(alert_id:str,db:Session=Depends(get_db)):
    obj=db.get(Alert,alert_id)
    if not obj: raise HTTPException(404,"Alert not found")
    return obj
@router.post("/{alert_id}/assign")
def assign_alert(alert_id:str,owner_id:str,db:Session=Depends(get_db)):
    obj=db.get(Alert,alert_id)
    if not obj: raise HTTPException(404,"Alert not found")
    obj.status="assigned"
    from app.services.audit_service import record
    record(db,owner_id,"alert_assigned","alert",alert_id,after={"owner_id":owner_id})
    db.commit(); return {"status":obj.status,"owner_id":owner_id}
