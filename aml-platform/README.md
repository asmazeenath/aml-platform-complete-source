# AML Transaction Monitoring & Investigation Platform

This repository follows the requested modular-monolith-first layout and implements the main workflow: REST transaction ingestion with event idempotency, PostgreSQL persistence, configurable starter scenarios, rolling account features, optional Isolation Forest scoring, NetworkX account relationships, weighted risk aggregation, evidence-bearing alerts, case creation/assignment notes/disposition, audit events, React investigator console, synthetic data generation, and Docker Compose infrastructure.

## Run locally
1. Copy `.env.example` to `.env`.
2. Start infrastructure: `docker compose up --build`.
3. In another terminal, install API requirements: `pip install -r apps/api/requirements.txt`.
4. Seed fictional customers/accounts: `python data/synthetic/seed_demo.py`.
5. Generate sample events: `python data/synthetic/generate_transactions.py`.
6. Start API locally if not using Compose: `cd apps/api && uvicorn app.main:app --reload`.
7. Start UI locally: `cd apps/web && npm install && npm run dev`.
8. API docs: http://localhost:8000/docs ; UI: http://localhost:5173.

Post events to `POST /api/v1/transactions`. Event JSON schema is in `data/schemas/transaction-event.schema.json`. Query alerts, cases, metrics and audit from the API docs.

## Scope notes
This is a portfolio implementation baseline, not production AML software. The Kafka consumer, Redis use, complete scenario administration/approval API, full auth/OIDC/MFA, sanctions/name screening, advanced reporting, model registry, DLQ/replay, observability exporters, and immutable audit storage require further integration/hardening. A development role-header placeholder is not real authentication. Review and migrate schema with Alembic before production.

All thresholds and synthetic profiles are illustrative. A risk score is only a prioritization aid and must not be interpreted as a finding of criminal conduct. Use only synthetic or properly authorized data.
