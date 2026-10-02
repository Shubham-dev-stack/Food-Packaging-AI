"""Standardized API exception handlers and error response formatters."""

import logging
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def create_error_response(
    error_code: str,
    message: str,
    details: list[dict[str, Any]] | None = None,
    error_id: str | None = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> JSONResponse:
    """Construct a consistent JSON error response."""
    content: dict[str, Any] = {
        "error": error_code,
        "message": message,
        "details": details or [],
    }
    if error_id:
        content["error_id"] = error_id
    return JSONResponse(status_code=status_code, content=content)


def register_exception_handlers(app: FastAPI) -> None:
    """Register uniform exception handlers on the FastAPI application."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors cleanly without raw tracebacks."""
        formatted_details: list[dict[str, Any]] = []
        for error in exc.errors():
            loc = error.get("loc", ())
            field_name = ".".join(str(elem) for elem in loc if elem != "body") or None
            formatted_details.append(
                {
                    "field": field_name,
                    "issue": error.get("msg", "Invalid value"),
                }
            )

        return create_error_response(
            error_code="VALIDATION_ERROR",
            message="Invalid request input parameters provided.",
            details=formatted_details,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Handle standard HTTP exceptions with structured response format."""
        error_code = "HTTP_ERROR"
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            error_code = "NOT_FOUND"
        elif exc.status_code == status.HTTP_400_BAD_REQUEST:
            error_code = "BAD_REQUEST"

        message = str(exc.detail) if isinstance(exc.detail, str) else "An HTTP error occurred."
        details = []
        if isinstance(exc.detail, list):
            details = exc.detail
        elif isinstance(exc.detail, dict):
            details = [exc.detail]

        return create_error_response(
            error_code=error_code,
            message=message,
            details=details,
            status_code=exc.status_code,
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Intercept unexpected internal exceptions, log them, and redact secrets/tracebacks."""
        error_id = str(uuid.uuid4())
        logger.exception("Unhandled server exception [error_id=%s]: %s", error_id, exc)

        return create_error_response(
            error_code="INTERNAL_SERVER_ERROR",
            message=(
                "An unexpected internal server error occurred. "
                "Please reference the error ID when reporting."
            ),
            error_id=error_id,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
