# Architecture
Payment source -> REST ingestion/Kafka boundary -> validation and idempotency -> PostgreSQL transaction store
-> rolling features -> deterministic scenarios + anomaly model + graph signals -> weighted risk aggregation
-> alert and case workflow -> React investigator console. Audit events preserve actor, action, entity and before/after data.
Build as a modular monolith first; scale stream processing and graph storage only when measured workload requires it.
