from datetime import date

import pytest
from sqlalchemy import func, insert, inspect, select
from sqlalchemy.exc import IntegrityError

from services.storage.init_db import init_db
from services.storage.models import Asset, Price
from services.storage.repository import seed_assets


def test_all_tables_created(engine):
    """Test that the schema contains every expected table."""
    tables = set(inspect(engine).get_table_names())
    assert {"assets", "prices", "news", "news_tickers"} <= tables


def test_seed_assets_is_idempotent(engine):
    """Test that seeding twice does not duplicate assets."""
    sectors = {"semiconductors": {"tickers": ["NVDA", "amd"]}}
    seed_assets(engine, sectors)
    seed_assets(engine, sectors)

    with engine.connect() as conn:
        tickers = conn.execute(select(Asset.ticker).order_by(Asset.ticker)).scalars().all()
    assert tickers == ["AMD", "NVDA"]


def test_init_db_seeds_watchlist(engine):
    """Test that init_db seeds tickers from configs/settings.yaml."""
    init_db(engine)
    with engine.connect() as conn:
        count = conn.execute(select(func.count()).select_from(Asset)).scalar()
    assert count >= 3


def test_price_requires_existing_asset(engine):
    """Test that a price cannot reference an unknown ticker."""
    row = {
        "ticker": "UNKNOWN",
        "date": date(2026, 1, 2),
        "interval": "1d",
        "open": 1.0,
        "high": 1.0,
        "low": 1.0,
        "close": 1.0,
        "volume": 1,
        "source": "test",
    }
    with pytest.raises(IntegrityError), engine.begin() as conn:
        conn.execute(insert(Price).values(row))
