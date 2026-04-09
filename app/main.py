import os
from dotenv import load_dotenv
load_dotenv()  # Only needed locally — Railway ignores this

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