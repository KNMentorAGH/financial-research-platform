"""Sentiment service - analyzes sentiment of news articles using FinBERT."""

import logging

logger = logging.getLogger(__name__)


def run() -> None:
    """Run sentiment analysis pipeline step.

    Contract:
        Input:  news articles from PostgreSQL
        Output: sentiment scores saved to PostgreSQL

    Raises:
        NotImplementedError: To be implemented by AI/ML Engineer.
    """
    logger.info("Starting sentiment analysis pipeline step")

    # TODO: implement actual sentiment analysis

    raise NotImplementedError("Sentiment service - to be implemented by AI/ML Engineer")
