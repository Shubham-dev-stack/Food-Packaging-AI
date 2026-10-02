"""Endpoints for querying food commodities and their postharvest properties."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.db import get_db
from backend.app.repositories.commodity_repository import CommodityRepository
from backend.app.schemas.commodity import CommodityBriefResponse, CommodityDetailResponse

router = APIRouter(prefix="/commodities", tags=["Commodities"])


@router.get("", response_model=list[CommodityBriefResponse])
def list_commodities(
    category: str | None = Query(
        default=None,
        description="Filter commodities by category (e.g., 'fruit', 'vegetable', 'snack_fried')",
    ),
    db: Session = Depends(get_db),
) -> list[CommodityBriefResponse]:
    """Retrieve all supported commodities in the knowledge base, optionally filtered by category."""
    commodities = CommodityRepository.list_all(db, category=category)
    return [CommodityBriefResponse.model_validate(c) for c in commodities]


@router.get("/{commodity_id}", response_model=CommodityDetailResponse)
def get_commodity(
    commodity_id: str,
    db: Session = Depends(get_db),
) -> CommodityDetailResponse:
    """Retrieve detailed physicochemical and respiration parameters for a specific commodity."""
    commodity = CommodityRepository.get_by_id(db, commodity_id=commodity_id)
    if not commodity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Commodity with ID '{commodity_id}' not found.",
        )
    return CommodityDetailResponse.model_validate(commodity)
