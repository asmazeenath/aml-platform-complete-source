FEATURE_NAMES=["in_count","out_count","in_amount","out_amount","unique_senders","unique_beneficiaries","out_in_ratio"]
def to_vector(features): return [float(features.get(k,0)) for k in FEATURE_NAMES]
