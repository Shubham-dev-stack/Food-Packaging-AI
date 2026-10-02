"""FastAPI application entrypoint, middleware, exception handlers, and routing."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.errors import register_exception_handlers
from backend.app.api.v1.router import api_router
from backend.app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Based Intelligent Food Packaging Material Recommendation System API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
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
