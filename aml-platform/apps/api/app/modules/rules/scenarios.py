# All starter thresholds are synthetic demo parameters, not official regulatory thresholds.
DEFAULT_SCENARIOS={
 "high_velocity":{"enabled":True,"version":1,"min_in_count":8,"min_senders":5,"window_minutes":60},
 "fan_out":{"enabled":True,"version":1,"min_beneficiaries":4,"window_minutes":60},
 "rapid_movement":{"enabled":True,"version":1,"min_out_in_ratio":0.8,"window_minutes":60},
 "profile_mismatch":{"enabled":False,"version":1,"volume_multiple":4}
}
def evaluate_scenarios(features, scenarios=DEFAULT_SCENARIOS):
    hits=[]
    p=scenarios["high_velocity"]
    if p["enabled"] and features["in_count"]>=p["min_in_count"] and features["unique_senders"]>=p["min_senders"]:
        hits.append({"scenario":"high_velocity","version":p["version"],"observed":features,
          "reason":f'{features["in_count"]} incoming transfers from {features["unique_senders"]} senders in {p["window_minutes"]} minutes'})
    p=scenarios["fan_out"]
    if p["enabled"] and features["unique_beneficiaries"]>=p["min_beneficiaries"]:
        hits.append({"scenario":"fan_out","version":p["version"],"observed":features,
          "reason":f'{features["unique_beneficiaries"]} distinct outgoing beneficiaries in {p["window_minutes"]} minutes'})
    p=scenarios["rapid_movement"]
    if p["enabled"] and features["out_in_ratio"]>=p["min_out_in_ratio"] and features["in_amount"]>0:
        hits.append({"scenario":"rapid_movement","version":p["version"],"observed":features,
          "reason":f'Outflow/inflow ratio is {features["out_in_ratio"]:.2f} in {p["window_minutes"]} minutes'})
    return hits
