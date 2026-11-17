from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.contracts import TransactionEvent
from app.modules.ingestion.service import ingest_event
router=APIRouter(prefix="/api/v1/transactions",tags=["transactions"])
@router.post("")
def create_transaction(event:TransactionEvent,db:Session=Depends(get_db)):
    return ingest_event(db,event)
