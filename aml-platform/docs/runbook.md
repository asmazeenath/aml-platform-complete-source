# Local runbook
1. Copy `.env.example` to `.env` and review values.
2. `docker compose up --build`.
3. Seed fictional customers/accounts with `python data/synthetic/seed_demo.py`.
4. Generate `transactions.json` with `python data/synthetic/generate_transactions.py`.
5. Post events to `POST /api/v1/transactions`; inspect `/docs`, `/api/v1/alerts`, `/api/v1/cases`.
6. Monitor API logs and PostgreSQL health. For production, add Kafka retries/DLQ, metrics, backups and access controls.
