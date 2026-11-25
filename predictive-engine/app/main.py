from fastapi import FastAPI
from datetime import datetime, timezone
from app.api.routes.equipment import router as equipment_router
from app.api.routes.assessments import router as assessments_router
from app.api.routes.assessments import (
    assessment_execution_router,
)

app = FastAPI(
    title="MAINTAINX Predictive Intelligence API",
    description=(
        "Predictive industrial equipment intelligence "
        "for mining cone crushers."
    ),
    version="0.1.0",
)

app.include_router(equipment_router)
app.include_router(assessments_router)
app.include_router(assessment_execution_router)

@app.get("/")
async def root():
    return {
        "application": "MAINTAINX",
        "service": "Predictive Intelligence Engine",
        "version": "0.1.0",
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "predictive-engine",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
