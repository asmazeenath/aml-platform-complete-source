import uuid
from app.models.entities import AuditEvent
def record(db, actor, action, entity_type, entity_id, before=None, after=None):
    db.add(AuditEvent(id=str(uuid.uuid4()),actor_id=actor,action=action,entity_type=entity_type,
                      entity_id=entity_id,before_json=before or {},after_json=after or {}))
