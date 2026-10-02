from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.db import get_db


class HealthResponse(BaseModel):
    status: str
    version: str
    service: str
    environment: str
    database: str


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health(db: Session = Depends(get_db)) -> HealthResponse:
    """Return health and readiness status of the backend API and database."""
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unavailable"

    overall_status = "healthy" if db_status == "connected" else "degraded"

    return HealthResponse(
        status=overall_status,
        version="0.1.0",
        service="food-packaging-ai-backend",
        environment=settings.ENVIRONMENT,
        database=db_status,
    )
