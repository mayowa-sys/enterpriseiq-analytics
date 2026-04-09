from app.db import db  # This triggers load_dotenv in db.py first
from fastapi import FastAPI
from app.routes.analytics import router as analytics_router

app = FastAPI(
    title="EnterpriseIQ Analytics Service",
    description="Internal analytics microservice for EnterpriseIQ",
    version="1.0.0"
)

@app.get("/health")
async def health():
    return {
        "status": "success",
        "message": "EnterpriseIQ Analytics Service is running"
    }

app.include_router(analytics_router, prefix="/analytics")