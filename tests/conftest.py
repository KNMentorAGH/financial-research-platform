import pytest
from sqlalchemy import create_engine, event

from services.storage.models import Base


@pytest.fixture
def engine():
    """In-memory SQLite engine with the full schema (no PostgreSQL needed in CI)."""
    engine = create_engine("sqlite:///:memory:")

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_conn, _):
        dbapi_conn.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()
