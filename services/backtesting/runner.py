"""Backtesting service - evaluates strategy performance on historical data."""

import logging

logger = logging.getLogger(__name__)


def run() -> None:
    """Run backtesting pipeline step.

    Contract:
        Input:  historical predictions and prices from PostgreSQL
        Output: performance metrics saved to results storage

    Raises:
        NotImplementedError: To be implemented by AI/ML Engineer.
    """
    logger.info("Starting backtesting pipeline step")

    # TODO: implement actual backtesting

    raise NotImplementedError("Backtesting service - to be implemented by AI/ML Engineer")
