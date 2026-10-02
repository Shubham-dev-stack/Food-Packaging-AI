"""Central API v1 router registering all domain endpoint resources."""

from fastapi import APIRouter

from backend.app.api.v1.commodities import router as commodities_router
from backend.app.api.v1.evidence import router as evidence_router
from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.materials import router as materials_router
from backend.app.api.v1.recommendations import router as recommendations_router

api_router = APIRouter()

# Register core health endpoint
api_router.include_router(health_router, tags=["Health"])

# Register domain resource endpoints
api_router.include_router(commodities_router)
api_router.include_router(materials_router)
api_router.include_router(evidence_router)
api_router.include_router(recommendations_router)
