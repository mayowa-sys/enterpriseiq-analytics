import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes.analytics import router as analytics_router

load_dotenv()

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