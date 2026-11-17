Alembic migration directory. Initialize with `alembic init migrations`, configure
`target_metadata = Base.metadata` from `app.core.database`, then generate migrations
with `alembic revision --autogenerate -m "initial schema"` and apply with `alembic upgrade head`.
The API currently creates tables for local development; production must use reviewed migrations.
