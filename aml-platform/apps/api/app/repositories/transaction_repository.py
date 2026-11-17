from sqlalchemy import select
from app.models.entities import Transaction
class TransactionRepository:
    def __init__(self, db): self.db=db
    def by_event_id(self, event_id):
        return self.db.scalar(select(Transaction).where(Transaction.event_id==event_id))
    def recent(self, account_id, since):
        return list(self.db.scalars(select(Transaction).where(
            ((Transaction.source_account_id==account_id)|(Transaction.destination_account_id==account_id)),
            Transaction.occurred_at>=since).order_by(Transaction.occurred_at.desc())))
