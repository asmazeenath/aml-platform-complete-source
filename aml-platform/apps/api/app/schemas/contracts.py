from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
class TransactionEvent(BaseModel):
    event_id: str = Field(min_length=1, max_length=120)
    source_account_ref: str
    destination_account_ref: str
    amount: Decimal = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    channel: str
    occurred_at: datetime
class CaseCreate(BaseModel):
    alert_ids: list[str] = Field(min_length=1)
    owner_id: str = "unassigned"
    priority: str = "medium"
class CaseNoteIn(BaseModel):
    author_id: str
    note: str = Field(min_length=2, max_length=5000)
class DispositionIn(BaseModel):
    actor_id: str
    disposition: str
    note: str = ""
class RuleConfig(BaseModel):
    rule_key: str
    version: int = 1
    enabled: bool = True
    parameters: dict
    approved_by: str
class ORMModel(BaseModel):
    model_config=ConfigDict(from_attributes=True)
