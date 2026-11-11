"""
Database session management for AgriSense AI.
Uses SQLAlchemy 2.0 with safe connection handling.
Designed to integrate smoothly with Dhyan's database foundation.
"""

from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from backend.app.core.config import settings
from backend.app.core.logging_config import logger

Base = declarative_base()

try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=False,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.warning(
        f"Database engine initialization deferred or offline: {e}. "
        "Shared PostgreSQL service can be configured via DATABASE_URL."
    )
    engine = None
    SessionLocal = None


def get_db() -> Generator[Session | None, None, None]:
    """Dependency generator providing transactional database sessions."""
    if SessionLocal is None:
        logger.debug("Database session requested but SessionLocal is unconfigured.")
        yield None
        return

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    """Verifies active connectivity to PostgreSQL database server."""
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.info(f"Database server currently unreachable ({e}). Operating in standalone/inference mode.")
        return False
