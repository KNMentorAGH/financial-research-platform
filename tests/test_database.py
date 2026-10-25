import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine

from apps.api.config import Settings
from apps.api.routers import health
from services.storage import database


def test_database_url_built_from_settings():
    """Test that the connection URL contains all values from settings."""
    s = Settings(
        postgres_host="db",
        postgres_port=6543,
        postgres_db="test_db",
        postgres_user="user",
        postgres_password="p@ss",
    )
    url = s.database_url

    assert url.drivername == "postgresql+psycopg2"
    assert url.host == "db"
    assert url.port == 6543
    assert url.database == "test_db"
    assert url.username == "user"
    assert url.password == "p@ss"
    assert "p%40ss" in url.render_as_string(hide_password=False)


def test_check_connection_ok():
    """Test that check_connection returns True for a reachable database."""
    engine = create_engine("sqlite:///:memory:")
    assert database.check_connection(engine) is True


def test_check_connection_unreachable():
    """Test that check_connection returns False when the database is unreachable."""
    engine = create_engine("postgresql+psycopg2://u:p@127.0.0.1:1/none?connect_timeout=1")
    assert database.check_connection(engine) is False


def test_health_db_endpoint(monkeypatch):
    """Test that /health/db maps the connection status to a response or 503."""
    monkeypatch.setattr(health, "check_connection", lambda: True)
    assert health.database_health_check()["database"] == "connected"

    monkeypatch.setattr(health, "check_connection", lambda: False)
    with pytest.raises(HTTPException) as exc:
        health.database_health_check()
    assert exc.value.status_code == 503
