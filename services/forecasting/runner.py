"""Forecasting service - predicts price direction."""

import logging

logger = logging.getLogger(__name__)


def run() -> None:
    """Run forecasting pipeline step.

    Contract:
        Input:  features (prices + sentiment) from PostgreSQL
        Output: predictions saved to PostgreSQL

    Raises:
        NotImplementedError: To be implemented by AI/ML Engineer.
    """
    logger.info("Starting forecasting pipeline step")

    # TODO: implement actual forecasting

    raise NotImplementedError("Forecasting service - to be implemented by AI/ML Engineer")
