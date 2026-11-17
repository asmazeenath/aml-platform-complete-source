from app.modules.scoring.risk import aggregate_risk
def test_risk_score_is_bounded():
    score,components=aggregate_risk(100,100,100,100)
    assert score==100
    assert set(components)=={"rule_score","anomaly_score","graph_score","customer_risk_factor"}
