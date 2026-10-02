"""Pydantic schemas for EvidenceSource entities."""

from pydantic import BaseModel, ConfigDict, Field


class EvidenceSourceResponse(BaseModel):
    """Bibliographic evidence entity ensuring every property and rule is cited."""

    model_config = ConfigDict(from_attributes=True)

    reference_id: str = Field(..., description="Unique alphanumeric reference identifier")
    citation_short: str = Field(..., description="Author and year format short citation")
    title: str = Field(..., description="Full publication title or standard designation")
    authors: str | None = Field(default=None, description="Primary authors or issuing organization")
    publication_year: int | None = Field(default=None, description="Year of publication")
    source_type: str = Field(..., description="Category of evidence source")
    doi_or_standard_number: str | None = Field(
        default=None, description="Official DOI or standard number"
    )
    notes: str | None = Field(
        default=None, description="Additional context or experimental conditions"
    )
