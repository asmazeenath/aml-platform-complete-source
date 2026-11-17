"""Temporal evaluation scaffold. Report precision@capacity, alert volume, recall on available labels and stability."""
def evaluate(y_true, scores, capacity):
    ranked=sorted(zip(scores,y_true),reverse=True)[:capacity]
    tp=sum(label==1 for _,label in ranked)
    return {"analyst_capacity":capacity,"precision_at_capacity":tp/max(len(ranked),1),
            "reviewed_alerts":len(ranked),"warning":"Metrics depend on the quality and completeness of review labels."}
