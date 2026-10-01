"""Repository abstraction for Commodity and related entities."""

from sqlalchemy.orm import Session, joinedload

from backend.app.models.commodity import Commodity


class CommodityRepository:
    """Data access methods for food commodities and their properties."""

    @staticmethod
    def get_by_id(db: Session, commodity_id: str) -> Commodity | None:
        return (
            db.query(Commodity)
            .options(
                joinedload(Commodity.property),
                joinedload(Commodity.respiration_data),
                joinedload(Commodity.map_configuration),
            )
            .filter(Commodity.commodity_id == commodity_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, common_name: str) -> Commodity | None:
        return (
            db.query(Commodity)
            .options(
                joinedload(Commodity.property),
                joinedload(Commodity.respiration_data),
                joinedload(Commodity.map_configuration),
            )
            .filter(Commodity.common_name == common_name)
            .first()
        )

    @staticmethod
    def list_all(db: Session, category: str | None = None) -> list[Commodity]:
        query = db.query(Commodity).options(
            joinedload(Commodity.property),
            joinedload(Commodity.respiration_data),
            joinedload(Commodity.map_configuration),
        )
        if category:
            query = query.filter(Commodity.category == category)
        return query.order_by(Commodity.common_name).all()

    @staticmethod
    def create(db: Session, commodity: Commodity) -> Commodity:
        db.add(commodity)
        db.commit()
        db.refresh(commodity)
        return commodity
