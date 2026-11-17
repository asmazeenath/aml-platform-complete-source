import uuid
from fastapi import HTTPException
from app.models.entities import Account, Transaction
from app.repositories.transaction_repository import TransactionRepository
from app.services.audit_service import record
from app.modules.monitoring.pipeline import monitor_transaction
def ingest_event(db, event):
    repo=TransactionRepository(db)
    if repo.by_event_id(event.event_id):
        return {"status":"duplicate_ignored","event_id":event.event_id,"alerts":[]}
    src=db.query(Account).filter_by(account_ref=event.source_account_ref).first()
    dst=db.query(Account).filter_by(account_ref=event.destination_account_ref).first()
    if not src or not dst: raise HTTPException(404,"Unknown account reference")
    tx=Transaction(id=str(uuid.uuid4()),event_id=event.event_id,source_account_id=src.id,
        destination_account_id=dst.id,amount=event.amount,currency=event.currency.upper(),
        channel=event.channel,occurred_at=event.occurred_at)
    db.add(tx); db.flush()
    result=monitor_transaction(db,tx)
    record(db,"system","transaction_ingested","transaction",tx.id,after={"event_id":event.event_id})
    db.commit()
    return {"status":"processed","transaction_id":tx.id,"alerts":result}
