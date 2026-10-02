"""Database engine, session management, and lifecycle hooks."""

import sqlite3
from collections.abc import Generator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.app.core.config import settings


class Base(DeclarativeBase):
    """Declarative base class for all SQLAlchemy ORM models."""

    pass


# SQLite-specific connect hook to strictly enforce relational foreign keys
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Create engine based on environment configuration
# check_same_thread=False is required for SQLite when handling multiple threads in FastAPI/Pytest
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    # Ensure parent directory exists if database file is located in a subfolder
    sqlite_file = settings.DATABASE_URL.replace("sqlite:///", "")
    if sqlite_file and sqlite_file != ":memory:":
        from pathlib import Path

        db_path = Path(sqlite_file)
        if db_path.parent and not db_path.parent.exists():
            db_path.parent.mkdir(parents=True, exist_ok=True)
else:
    connect_args = {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for obtaining a transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(target_engine: Engine | None = None) -> None:
    """Initialize database tables in the target engine."""
    eng = target_engine or engine
    Base.metadata.create_all(bind=eng)


def drop_db(target_engine: Engine | None = None) -> None:
    """Drop all tables in the target engine (useful for test resets)."""
    eng = target_engine or engine
    Base.metadata.drop_all(bind=eng)
