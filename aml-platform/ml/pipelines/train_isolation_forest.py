import argparse, json
from app.modules.scoring.anomaly import train_baseline
def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--output",default="ml/model_artifacts/isolation_forest.joblib")
    a=p.parse_args()
    with open(a.input,encoding="utf-8") as f: rows=json.load(f)
    print(train_baseline(rows,a.output))
if __name__=="__main__": main()
