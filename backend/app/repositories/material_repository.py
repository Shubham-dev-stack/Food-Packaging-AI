"""Repository abstraction for PackagingMaterial and barrier properties."""

from sqlalchemy.orm import Session, joinedload

from backend.app.models.material import PackagingMaterial


class MaterialRepository:
    """Data access methods for packaging materials, barrier data, and sustainability metrics."""

    @staticmethod
    def get_by_id(db: Session, material_id: str) -> PackagingMaterial | None:
        return (
            db.query(PackagingMaterial)
            .options(
                joinedload(PackagingMaterial.barrier_properties),
                joinedload(PackagingMaterial.sustainability_metric),
                joinedload(PackagingMaterial.cost_index),
            )
            .filter(PackagingMaterial.material_id == material_id)
            .first()
        )

    @staticmethod
    def get_by_trade_code(db: Session, trade_code: str) -> PackagingMaterial | None:
        return (
            db.query(PackagingMaterial)
            .options(
                joinedload(PackagingMaterial.barrier_properties),
                joinedload(PackagingMaterial.sustainability_metric),
                joinedload(PackagingMaterial.cost_index),
            )
            .filter(PackagingMaterial.trade_code == trade_code)
            .first()
        )

    @staticmethod
    def list_all(db: Session, family: str | None = None) -> list[PackagingMaterial]:
        query = db.query(PackagingMaterial).options(
            joinedload(PackagingMaterial.barrier_properties),
            joinedload(PackagingMaterial.sustainability_metric),
            joinedload(PackagingMaterial.cost_index),
        )
        if family:
            query = query.filter(PackagingMaterial.material_family == family)
        return query.order_by(PackagingMaterial.material_id).all()

    @staticmethod
    def create(db: Session, material: PackagingMaterial) -> PackagingMaterial:
        db.add(material)
        db.commit()
        db.refresh(material)
        return material
