from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.entities import AuditEvent
router=APIRouter(prefix="/api/v1/audit",tags=["audit"])
@router.get("")
def audit_events(limit:int=100,db:Session=Depends(get_db)):
    return list(db.scalars(select(AuditEvent).order_by(AuditEvent.occurred_at.desc()).limit(min(max(limit,1),500))))
