import logging
from functools import lru_cache

import yaml

logger = logging.getLogger(__name__)


@lru_cache
def get_settings() -> dict:
    """Load and cache application settings from configuration file.

    Returns:
        Dictionary with application settings.
    """
    with open("configs/settings.yaml") as f:
        return yaml.safe_load(f)


def get_watchlist() -> list[str]:
    """Get flat list of all tickers from watchlist configuration.

    Returns:
        List of ticker symbols (e.g. ['NVDA', 'AMD', 'INTC']).
    """
    settings = get_settings()
    tickers = []

    for sector in settings["watchlist"]["sectors"].values():
        tickers.extend(sector["tickers"])

    return tickers
