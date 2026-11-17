from sqlalchemy import String, DateTime, Numeric, ForeignKey, Text, JSON, Boolean, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.core.database import Base
def utcnow(): return datetime.now(timezone.utc)
class Customer(Base):
    __tablename__="customers"
    id: Mapped[str]=mapped_column(String(36), primary_key=True)
    customer_ref: Mapped[str]=mapped_column(String(80), unique=True)
    customer_type: Mapped[str]=mapped_column(String(30), default="individual")
    onboarding_date: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
    occupation_or_business: Mapped[str]=mapped_column(String(160), default="Not supplied")
    expected_activity_band: Mapped[str]=mapped_column(String(40), default="standard")
    risk_rating: Mapped[str]=mapped_column(String(20), default="medium")
    kyc_status: Mapped[str]=mapped_column(String(30), default="pending")
class Account(Base):
    __tablename__="accounts"
    id: Mapped[str]=mapped_column(String(36), primary_key=True)
    customer_id: Mapped[str]=mapped_column(ForeignKey("customers.id"))
    account_ref: Mapped[str]=mapped_column(String(80), unique=True)
    currency: Mapped[str]=mapped_column(String(3), default="INR")
    opened_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
    status: Mapped[str]=mapped_column(String(20), default="active")
class Transaction(Base):
    __tablename__="transactions"
    id: Mapped[str]=mapped_column(String(36), primary_key=True)
    event_id: Mapped[str]=mapped_column(String(120), unique=True, index=True)
    source_account_id: Mapped[str]=mapped_column(String(36), index=True)
    destination_account_id: Mapped[str]=mapped_column(String(36), index=True)
    amount: Mapped[float]=mapped_column(Numeric(20,2))
    currency: Mapped[str]=mapped_column(String(3))
    channel: Mapped[str]=mapped_column(String(40))
    occurred_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), index=True)
    ingested_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
class FeatureSnapshot(Base):
    __tablename__="features_snapshots"
    id: Mapped[str]=mapped_column(String(36), primary_key=True)
    account_id: Mapped[str]=mapped_column(String(36), index=True)
    window_start: Mapped[datetime]=mapped_column(DateTime(timezone=True))
    window_end: Mapped[datetime]=mapped_column(DateTime(timezone=True))
    feature_json: Mapped[dict]=mapped_column(JSON)
    computed_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
class RuleDefinition(Base):
    __tablename__="rule_definitions"
    id: Mapped[str]=mapped_column(String(36), primary_key=True)
    rule_key: Mapped[str]=mapped_column(String(100), index=True)
    version: Mapped[int]=mapped_column(Integer, default=1)
    enabled: Mapped[bool]=mapped_column(Boolean, default=True)
    parameters_json: Mapped[dict]=mapped_column(JSON)
    effective_from: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
    approved_by: Mapped[str]=mapped_column(String(100), default="demo-admin")
class Alert(Base):
    __tablename__="alerts"
    id: Mapped[str]=mapped_column(String(36), primary_key=True)
    alert_ref: Mapped[str]=mapped_column(String(80), unique=True)
    account_id: Mapped[str]=mapped_column(String(36), index=True)
    transaction_id: Mapped[str]=mapped_column(String(36), index=True)
    scenario_key: Mapped[str]=mapped_column(String(300))
    severity: Mapped[str]=mapped_column(String(20))
    score: Mapped[float]=mapped_column(Float)
    reasons_json: Mapped[dict]=mapped_column(JSON)
    evidence_json: Mapped[dict]=mapped_column(JSON)
    status: Mapped[str]=mapped_column(String(30), default="open")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
class Case(Base):
    __tablename__="cases"
    id: Mapped[str]=mapped_column(String(36), primary_key=True)
    case_ref: Mapped[str]=mapped_column(String(80), unique=True)
    priority: Mapped[str]=mapped_column(String(20))
    owner_id: Mapped[str]=mapped_column(String(100), default="unassigned")
    status: Mapped[str]=mapped_column(String(30), default="open")
    disposition: Mapped[str|None]=mapped_column(String(80), nullable=True)
    opened_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
    closed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True), nullable=True)
class CaseAlert(Base):
    __tablename__="case_alerts"
    id: Mapped[str]=mapped_column(String(36), primary_key=True)
    case_id: Mapped[str]=mapped_column(ForeignKey("cases.id"))
    alert_id: Mapped[str]=mapped_column(ForeignKey("alerts.id"))
class CaseNote(Base):
    __tablename__="case_notes"
    id: Mapped[str]=mapped_column(String(36), primary_key=True)
    case_id: Mapped[str]=mapped_column(ForeignKey("cases.id"))
    author_id: Mapped[str]=mapped_column(String(100))
    note: Mapped[str]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
class EvidenceItem(Base):
    __tablename__="evidence_items"
    id: Mapped[str]=mapped_column(String(36), primary_key=True)
    case_id: Mapped[str]=mapped_column(ForeignKey("cases.id"))
    evidence_type: Mapped[str]=mapped_column(String(60))
    reference: Mapped[str]=mapped_column(Text)
    content_hash: Mapped[str]=mapped_column(String(128))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
class AuditEvent(Base):
    __tablename__="audit_events"
    id: Mapped[str]=mapped_column(String(36), primary_key=True)
    actor_id: Mapped[str]=mapped_column(String(100))
    action: Mapped[str]=mapped_column(String(100))
    entity_type: Mapped[str]=mapped_column(String(60))
    entity_id: Mapped[str]=mapped_column(String(100))
    before_json: Mapped[dict]=mapped_column(JSON, default=dict)
    after_json: Mapped[dict]=mapped_column(JSON, default=dict)
    occurred_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
