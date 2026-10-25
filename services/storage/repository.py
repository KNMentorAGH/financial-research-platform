"""Data access layer - writing to and reading from the database."""

import logging
from collections.abc import Sequence
from typing import Any

from sqlalchemy import Engine, Table
from sqlalchemy.dialects import postgresql, sqlite

from services.storage.models import Asset

logger = logging.getLogger(__name__)


def upsert_rows(
    engine: Engine,
    table: Table,
    rows: Sequence[dict[str, Any]],
    conflict_columns: list[str],
    update_columns: list[str] | None = None,
) -> int:
    """Insert rows, skipping or updating the ones that already exist.

    Works on PostgreSQL (production) and SQLite (tests) via ON CONFLICT.

    Args:
        engine: SQLAlchemy engine.
        table: Target table.
        rows: Rows to insert as dictionaries (column name -> value).
        conflict_columns: Columns of the unique constraint / primary key.
        update_columns: Columns to overwrite on conflict. None means "do nothing".

    Returns:
        Number of rows inserted or updated.
    """
    if not rows:
        return 0

    dialect_insert = postgresql.insert if engine.dialect.name == "postgresql" else sqlite.insert
    stmt = dialect_insert(table).values(list(rows))

    if update_columns:
        stmt = stmt.on_conflict_do_update(
            index_elements=conflict_columns,
            set_={col: stmt.excluded[col] for col in update_columns},
        )
    else:
        stmt = stmt.on_conflict_do_nothing(index_elements=conflict_columns)

    with engine.begin() as conn:
        result = conn.execute(stmt)
    return max(result.rowcount or 0, 0)


def seed_assets(engine: Engine, sectors: dict[str, dict]) -> int:
    """Insert tracked tickers from the watchlist into the assets table.

    Args:
        engine: SQLAlchemy engine.
        sectors: Watchlist sectors, e.g. {"semiconductors": {"tickers": ["NVDA"]}}.

    Returns:
        Number of assets inserted or updated.
    """
    rows = [
        {"ticker": ticker.upper(), "sector": sector_name}
        for sector_name, sector in sectors.items()
        for ticker in sector["tickers"]
    ]
    return upsert_rows(
        engine, Asset.__table__, rows, conflict_columns=["ticker"], update_columns=["sector"]
    )
