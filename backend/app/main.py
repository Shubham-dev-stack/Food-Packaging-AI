"""FastAPI application entrypoint, middleware, exception handlers, and routing."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.errors import register_exception_handlers
from backend.app.api.v1.router import api_router
from backend.app.core.config import settings
from backend.app.core.db import init_db

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("food_packaging_ai")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Execute startup and shutdown tasks safely."""
    logger.info("Initializing database schema on startup...")
    try:
        init_db()
        logger.info("Database schema initialized successfully.")
    except Exception as e:
        logger.error("Failed to initialize database schema: %s", e)
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Based Intelligent Food Packaging Material Recommendation System API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Register uniform error handling across the application
register_exception_handlers(app)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router at configured prefix (default: /api)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root_status():
    return {
        "service": settings.PROJECT_NAME,
        "status": "online",
        "api_docs": "/docs",
        "health_check": f"{settings.API_V1_STR}/health",
    }
