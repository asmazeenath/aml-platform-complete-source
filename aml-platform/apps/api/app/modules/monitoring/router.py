from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.entities import Transaction, Alert, Case
router=APIRouter(prefix="/api/v1/metrics",tags=["metrics"])
@router.get("/aml")
def metrics(db:Session=Depends(get_db)):
    return {"transactions_processed":db.scalar(select(func.count()).select_from(Transaction)),
      "alerts_total":db.scalar(select(func.count()).select_from(Alert)),
      "open_alerts":db.scalar(select(func.count()).select_from(Alert).where(Alert.status.in_(["open","assigned","in_review"]))),
      "open_cases":db.scalar(select(func.count()).select_from(Case).where(Case.status!="closed"))}
