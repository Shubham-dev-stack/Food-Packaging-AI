"""Repository abstraction for EvidenceSource entities."""

from sqlalchemy.orm import Session

from backend.app.models.evidence import EvidenceSource


class EvidenceRepository:
    """Data access methods for bibliographic evidence sources."""

    @staticmethod
    def get_by_id(db: Session, reference_id: str) -> EvidenceSource | None:
        return db.query(EvidenceSource).filter(EvidenceSource.reference_id == reference_id).first()

    @staticmethod
    def list_all(db: Session) -> list[EvidenceSource]:
        return db.query(EvidenceSource).order_by(EvidenceSource.reference_id).all()

    @staticmethod
    def create(db: Session, source: EvidenceSource) -> EvidenceSource:
        db.add(source)
        db.commit()
        db.refresh(source)
        return source
