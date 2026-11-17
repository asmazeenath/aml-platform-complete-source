import json, random
from datetime import datetime, timedelta, timezone
random.seed(7)
now=datetime.now(timezone.utc)
events=[]
# Benign baseline events
for i in range(40):
    src=f"acct_{random.randint(1,10):03d}"; dst=f"acct_{random.randint(11,20):03d}"
    events.append({"event_id":f"synthetic_{i}","source_account_ref":src,"destination_account_ref":dst,
      "amount":f"{random.randint(100,5000):.2f}","currency":"INR","channel":"UPI",
      "occurred_at":(now-timedelta(minutes=random.randint(1,10000))).isoformat()})
# Illustrative fan-in/fan-out pattern; synthetic only
for i in range(15):
    events.append({"event_id":f"pattern_in_{i}","source_account_ref":f"acct_{i+1:03d}",
      "destination_account_ref":"acct_999","amount":"950.00","currency":"INR","channel":"IMPS",
      "occurred_at":(now-timedelta(minutes=35-i)).isoformat()})
for i in range(5):
    events.append({"event_id":f"pattern_out_{i}","source_account_ref":"acct_999",
      "destination_account_ref":f"acct_{i+30:03d}","amount":"2200.00","currency":"INR","channel":"IMPS",
      "occurred_at":(now-timedelta(minutes=3)).isoformat()})
with open("data/synthetic/transactions.json","w") as f: json.dump(events,f,indent=2)
print(f"Wrote {len(events)} synthetic events")
