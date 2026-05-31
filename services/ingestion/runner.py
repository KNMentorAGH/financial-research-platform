"""Ingestion service - fetches news and prices for tracked tickers."""

import logging

logger = logging.getLogger(__name__)


def run() -> None:
    """Run ingestion pipeline step.

    Contract:
        Input:  watchlist from configs/settings.yaml
        Output: raw data in data/raw/ and processed records in PostgreSQL

    Raises:
        NotImplementedError: To be implemented by Data Engineer.
    """
    logger.info("Starting ingestion pipeline step")

    # TODO: implement actual ingestion logic

    raise NotImplementedError("Ingestion service - to be implemented by Data Engineer")
