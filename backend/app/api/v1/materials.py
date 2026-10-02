"""Endpoints for querying packaging materials, barrier properties, and eco-metrics."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.db import get_db
from backend.app.repositories.material_repository import MaterialRepository
from backend.app.schemas.material import PackagingMaterialResponse

router = APIRouter(prefix="/materials", tags=["Materials"])


@router.get("", response_model=list[PackagingMaterialResponse])
def list_materials(
    family: str | None = Query(
        default=None,
        description="Filter packaging materials by polymer family (e.g., 'LDPE', 'PET')",
    ),
    db: Session = Depends(get_db),
) -> list[PackagingMaterialResponse]:
    """Retrieve all candidate packaging materials with barrier, eco, and cost metrics."""
    materials = MaterialRepository.list_all(db, family=family)
    return [PackagingMaterialResponse.model_validate(m) for m in materials]


@router.get("/{material_id}", response_model=PackagingMaterialResponse)
def get_material(
    material_id: str,
    db: Session = Depends(get_db),
) -> PackagingMaterialResponse:
    """Retrieve barrier specifications and lifecycle metrics for a specific packaging material."""
    material = MaterialRepository.get_by_id(db, material_id=material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Packaging material with ID '{material_id}' not found.",
        )
    return PackagingMaterialResponse.model_validate(material)
