import uuid
from datetime import timedelta
from app.models.entities import Alert, FeatureSnapshot, Customer
from app.modules.monitoring.features import account_features
from app.modules.rules.scenarios import evaluate_scenarios
from app.modules.graph.analytics import account_network
from app.modules.scoring.anomaly import anomaly_score
from app.modules.scoring.risk import aggregate_risk
from app.core.config import settings
def monitor_transaction(db, tx):
    features=account_features(db,tx.source_account_id,tx.occurred_at,60)
    hits=evaluate_scenarios(features)
    graph=account_network(db,tx.source_account_id,tx.occurred_at-timedelta(hours=24))
    anomaly,model_meta=anomaly_score(features,settings.model_path)
    rule_score=min(100,len(hits)*35)
    graph_score=min(100,graph["degree"]*8)
    customer=db.query(Customer).filter_by(id=db.query(__import__("app.models.entities",fromlist=["Account"]).Account).filter_by(id=tx.source_account_id).first().customer_id).first()
    customer_factor={"low":15,"medium":40,"high":75}.get((customer.risk_rating if customer else "medium").lower(),40)
    score,components=aggregate_risk(rule_score,anomaly,graph_score,customer_factor)
    if not hits and score<50: return []
    reasons=[{"code":h["scenario"].upper(),"message":h["reason"],"observed":h["observed"],"rule_version":h["version"]} for h in hits]
    if anomaly>=60: reasons.append({"code":"BEHAVIORAL_ANOMALY","message":"Activity deviates from the model's learned baseline","model":model_meta})
    if graph_score>=40: reasons.append({"code":"NETWORK_ACTIVITY","message":"Account has multiple connected counterparties","graph":graph})
    alert_id=str(uuid.uuid4()); ref="ALT-"+alert_id[:8].upper()
    evidence={"transaction_id":tx.id,"event_id":tx.event_id,"feature_snapshot":features,"graph_context":graph,
      "score_components":components,"model":model_meta,"rule_hits":hits,"score_timestamp":tx.occurred_at.isoformat()}
    db.add(FeatureSnapshot(id=str(uuid.uuid4()),account_id=tx.source_account_id,
      window_start=tx.occurred_at-timedelta(minutes=60),window_end=tx.occurred_at,feature_json=features))
    db.add(Alert(id=alert_id,alert_ref=ref,account_id=tx.source_account_id,transaction_id=tx.id,
      scenario_key=",".join(h["scenario"] for h in hits) or "behavioral_anomaly",
      severity="high" if score>=70 else "medium" if score>=40 else "low",
      score=score,reasons_json=reasons,evidence_json=evidence,status="open"))
    return [{"id":alert_id,"alert_ref":ref,"score":score,"severity":"high" if score>=70 else "medium" if score>=40 else "low","reasons":reasons}]
