"""Endpoints for generating and retrieving packaging recommendations."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.db import get_db
from backend.app.schemas.recommendation import RecommendationCreateRequest, RecommendationResponse
from backend.app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("", response_model=RecommendationResponse, status_code=status.HTTP_200_OK)
def create_recommendation(
    request_data: RecommendationCreateRequest,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    """Evaluate optimal packaging materials and technical specifications for given commodity."""
    try:
        return RecommendationService.create_recommendation(db, request_data)
    except ValueError as e:
        # Commodity not found or domain pre-condition violation
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.get("/{request_id}", response_model=RecommendationResponse)
def get_recommendation(
    request_id: str,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    """Retrieve a previously evaluated recommendation audit session by ID."""
    result = RecommendationService.get_recommendation_by_id(db, request_id=request_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation session with ID '{request_id}' not found.",
        )
    return result
