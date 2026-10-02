"""Standardized API error response models."""

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Specific error occurrence details."""

    field: str | None = Field(
        default=None, description="The input field associated with this error if applicable"
    )
    issue: str = Field(..., description="Human-readable description of the error")


class ErrorResponse(BaseModel):
    """Consistent JSON payload returned across all API error responses."""

    error: str = Field(..., description="High-level machine-readable error category")
    message: str = Field(..., description="Summary explanation of the error condition")
    details: list[ErrorDetail] = Field(
        default_factory=list, description="Specific contextual error details"
    )
    error_id: str | None = Field(
        default=None, description="Internal error tracking identifier for 500 errors"
    )
