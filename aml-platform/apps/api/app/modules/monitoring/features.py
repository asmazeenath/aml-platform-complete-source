from datetime import timedelta
from sqlalchemy import select
from app.models.entities import Transaction
def account_features(db, account_id, at, minutes=60):
    since=at-timedelta(minutes=minutes)
    rows=list(db.scalars(select(Transaction).where(Transaction.occurred_at>=since,
        ((Transaction.source_account_id==account_id)|(Transaction.destination_account_id==account_id)))))
    inbound=[t for t in rows if t.destination_account_id==account_id]
    outbound=[t for t in rows if t.source_account_id==account_id]
    return {"window_minutes":minutes,"in_count":len(inbound),"out_count":len(outbound),
      "in_amount":float(sum((t.amount for t in inbound),0)),"out_amount":float(sum((t.amount for t in outbound),0)),
      "unique_senders":len({t.source_account_id for t in inbound}),
      "unique_beneficiaries":len({t.destination_account_id for t in outbound}),
      "out_in_ratio":float(sum((t.amount for t in outbound),0)/max(sum((t.amount for t in inbound),0),1))}
