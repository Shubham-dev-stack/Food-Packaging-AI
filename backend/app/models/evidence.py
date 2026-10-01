"""EvidenceSource ORM model for scientific literature and standards traceability."""

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.db import Base


class EvidenceSource(Base):
    """Bibliographic evidence entity ensuring every property and rule is cited."""

    __tablename__ = "evidence_sources"

    reference_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    citation_short: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    authors: Mapped[str | None] = mapped_column(String(256), nullable=True)
    publication_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        # e.g., 'textbook', 'peer_reviewed_journal', 'standards_document',
        # 'government_compendium', 'manufacturer_tds'
    )
    doi_or_standard_number: Mapped[str | None] = mapped_column(String(128), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<EvidenceSource(id='{self.reference_id}', citation='{self.citation_short}')>"
