from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str
    service: str


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    """Return health status of the backend API."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        service="food-packaging-ai-backend",
    )
