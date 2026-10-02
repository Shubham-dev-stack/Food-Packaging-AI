"""Endpoints for querying bibliographic evidence sources and ASTM standards."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.db import get_db
from backend.app.repositories.evidence_repository import EvidenceRepository
from backend.app.schemas.evidence import EvidenceSourceResponse

router = APIRouter(prefix="/evidence", tags=["Evidence"])


@router.get("", response_model=list[EvidenceSourceResponse])
def list_evidence(db: Session = Depends(get_db)) -> list[EvidenceSourceResponse]:
    """Retrieve all bibliographic citations, ASTM testing standards, and scientific sources."""
    sources = EvidenceRepository.list_all(db)
    return [EvidenceSourceResponse.model_validate(s) for s in sources]


@router.get("/{reference_id}", response_model=EvidenceSourceResponse)
def get_evidence(
    reference_id: str,
    db: Session = Depends(get_db),
) -> EvidenceSourceResponse:
    """Retrieve details for a specific bibliographic citation or ASTM standard."""
    source = EvidenceRepository.get_by_id(db, reference_id=reference_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence source with ID '{reference_id}' not found.",
        )
    return EvidenceSourceResponse.model_validate(source)
