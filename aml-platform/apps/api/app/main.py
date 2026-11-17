from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.models import entities
from app.modules.ingestion.router import router as ingestion_router
from app.modules.alerts.router import router as alerts_router
from app.modules.cases.router import router as cases_router
from app.modules.audit.router import router as audit_router
from app.modules.monitoring.router import router as metrics_router
app=FastAPI(title=settings.app_name,version="1.0.0",description="Risk-based AML review platform. Scores prioritize review; they do not establish criminal conduct.")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins.split(","),allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
Base.metadata.create_all(bind=engine)
for router in [ingestion_router,alerts_router,cases_router,audit_router,metrics_router]: app.include_router(router)
@app.get("/health")
def health(): return {"status":"ok","service":settings.app_name}
