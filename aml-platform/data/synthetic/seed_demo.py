import os, sys, uuid
sys.path.insert(0,os.path.abspath("apps/api"))
from app.core.database import Base,engine,SessionLocal
from app.models.entities import Customer,Account
from datetime import datetime,timezone
Base.metadata.create_all(engine)
db=SessionLocal()
for i in range(1,41):
    cid=f"customer-{i:03d}"; aid=f"account-{i:03d}"
    if not db.get(Customer,cid):
        db.add(Customer(id=cid,customer_ref=f"CUST-{i:03d}",customer_type="individual",
          occupation_or_business="Synthetic profile",expected_activity_band="standard",
          risk_rating="medium" if i%5==0 else "low",kyc_status="verified"))
        db.add(Account(id=aid,customer_id=cid,account_ref=f"acct_{i:03d}",currency="INR"))
if not db.get(Customer,"customer-999"):
    db.add(Customer(id="customer-999",customer_ref="CUST-999",customer_type="individual",
      occupation_or_business="Synthetic profile",expected_activity_band="standard",risk_rating="medium",kyc_status="verified"))
    db.add(Account(id="account-999",customer_id="customer-999",account_ref="acct_999",currency="INR"))
for i in range(30,36):
    cid=f"customer-{i+1:03d}"; aid=f"account-{i+1:03d}"
    if not db.get(Customer,cid):
        db.add(Customer(id=cid,customer_ref=f"CUST-{i+1:03d}",customer_type="individual",
          occupation_or_business="Synthetic profile",expected_activity_band="standard",risk_rating="low",kyc_status="verified"))
        db.add(Account(id=aid,customer_id=cid,account_ref=f"acct_{i+1:03d}",currency="INR"))
db.commit(); db.close(); print("Seeded synthetic profiles.")
