import logging

import pandas as pd

from services.sentiment.baseline import SentimentBaselineEngine

logger = logging.getLogger(__name__)


def run() -> None:
    """Run sentiment analysis pipeline step."""
    logger.info("Starting sentiment analysis pipeline step")

    mock_news = pd.DataFrame(
        {
            "title": ["NVDA revenue surge beats expectations"],
            "ticker": ["NVDA"],
            "published_at": [pd.Timestamp.now()],
        }
    )

    engine = SentimentBaselineEngine()
    processed_df = engine.process_news_dataframe(mock_news)

    logger.info(f"Analyzed sentiment for {len(processed_df)} articles")
