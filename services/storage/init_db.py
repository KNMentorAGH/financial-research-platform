"""Create database tables and seed tracked assets.

Safe to run many times - existing tables and rows are kept.

Usage:
    python -m services.storage.init_db
"""

import logging

from sqlalchemy import Engine

from apps.api.dependencies import get_settings
from services.storage.database import get_engine
from services.storage.models import Base
from services.storage.repository import seed_assets

logger = logging.getLogger(__name__)


def init_db(engine: Engine | None = None) -> None:
    """Create all tables (if missing) and seed assets from the watchlist.

    Args:
        engine: Optional engine. Defaults to the shared PostgreSQL engine.
    """
    engine = engine or get_engine()

    Base.metadata.create_all(engine)
    logger.info(f"Tables ready: {sorted(Base.metadata.tables)}")

    sectors = get_settings()["watchlist"]["sectors"]
    count = seed_assets(engine, sectors)
    logger.info(f"Seeded {count} assets from watchlist")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    init_db()
