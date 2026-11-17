import networkx as nx
from sqlalchemy import select
from app.models.entities import Transaction
def account_network(db, account_id, since):
    rows=list(db.scalars(select(Transaction).where(Transaction.occurred_at>=since)))
    graph=nx.DiGraph()
    graph.add_edges_from((r.source_account_id,r.destination_account_id) for r in rows)
    if account_id not in graph: return {"degree":0,"fan_in":0,"fan_out":0,"component_size":1,"cycles":[]}
    undirected=graph.to_undirected()
    component=nx.node_connected_component(undirected,account_id)
    cycles=[c for c in nx.simple_cycles(graph) if len(c)<=4][:10]
    return {"degree":int(graph.degree(account_id)),"fan_in":int(graph.in_degree(account_id)),
      "fan_out":int(graph.out_degree(account_id)),"component_size":len(component),"cycles":cycles}
