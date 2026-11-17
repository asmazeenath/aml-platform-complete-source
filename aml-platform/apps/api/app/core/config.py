from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "AML Transaction Monitoring Platform"
    database_url: str = "postgresql+psycopg://aml:aml@localhost:5432/aml"
    redis_url: str = "redis://localhost:6379/0"
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic: str = "transactions.raw"
    cors_origins: str = "http://localhost:5173"
    model_path: str = "ml/model_artifacts/isolation_forest.joblib"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
