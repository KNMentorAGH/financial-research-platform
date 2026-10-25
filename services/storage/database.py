"""Database connection layer - shared SQLAlchemy engine and sessions for all services."""

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from apps.api.config import settings

logger = logging.getLogger(__name__)


@lru_cache
def get_engine(url: str | URL | None = None) -> Engine:
    """Create (once) and return SQLAlchemy engine.

    Args:
        url: Optional connection URL. Defaults to PostgreSQL URL built from settings.

    Returns:
        Cached SQLAlchemy engine.
    """
    return create_engine(
        url or settings.database_url,
        pool_pre_ping=True,
        future=True,
    )


def get_session_factory(engine: Engine | None = None) -> sessionmaker[Session]:
    """Return session factory bound to the given engine.

    Args:
        engine: Optional engine. Defaults to the shared engine from get_engine().

    Returns:
        Configured sessionmaker.
    """
    return sessionmaker(bind=engine or get_engine(), expire_on_commit=False)


@contextmanager
def session_scope(engine: Engine | None = None) -> Iterator[Session]:
    """Provide a transactional scope - commit on success, rollback on error.

    Args:
        engine: Optional engine. Defaults to the shared engine.

    Yields:
        Active SQLAlchemy session.
    """
    session = get_session_factory(engine)()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def check_connection(engine: Engine | None = None) -> bool:
    """Check whether the database is reachable.

    Args:
        engine: Optional engine. Defaults to the shared engine.

    Returns:
        True if a simple query succeeds, False otherwise.
    """
    try:
        with (engine or get_engine()).connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        return False
