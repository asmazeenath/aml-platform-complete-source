from app.modules.rules.scenarios import evaluate_scenarios
def test_fanin_triggers_velocity():
    features={"in_count":10,"unique_senders":8,"unique_beneficiaries":1,"out_in_ratio":0.1}
    assert "high_velocity" in [x["scenario"] for x in evaluate_scenarios(features)]
