def aggregate_risk(rule_score, anomaly_score, graph_score, customer_risk_factor):
    components={"rule_score":float(rule_score),"anomaly_score":float(anomaly_score),
      "graph_score":float(graph_score),"customer_risk_factor":float(customer_risk_factor)}
    score=0.45*components["rule_score"]+0.30*components["anomaly_score"]+0.15*components["graph_score"]+0.10*components["customer_risk_factor"]
    return round(min(100,max(0,score)),2),components
