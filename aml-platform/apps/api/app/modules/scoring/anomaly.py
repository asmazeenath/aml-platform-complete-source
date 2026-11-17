import os, joblib
import numpy as np
from sklearn.ensemble import IsolationForest
FEATURES=["in_count","out_count","in_amount","out_amount","unique_senders","unique_beneficiaries","out_in_ratio"]
def train_baseline(rows, path):
    X=np.array([[float(r.get(k,0)) for k in FEATURES] for r in rows])
    model=IsolationForest(n_estimators=150,contamination="auto",random_state=42).fit(X)
    os.makedirs(os.path.dirname(path),exist_ok=True); joblib.dump({"model":model,"features":FEATURES,"version":"iforest-1"},path)
    return path
def anomaly_score(features,path):
    if not os.path.exists(path): return 0.0,{"model_version":"not-trained","status":"baseline_unavailable"}
    bundle=joblib.load(path); model=bundle["model"]
    row=np.array([[float(features.get(k,0)) for k in bundle["features"]]])
    raw=float(-model.score_samples(row)[0])
    return round(max(0,min(100,raw*25)),2),{"model_version":bundle["version"],"raw_anomaly":raw}
