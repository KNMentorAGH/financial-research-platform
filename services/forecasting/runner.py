import logging

from apps.api.dependencies import get_watchlist
from services.forecasting.data_processor import MarketDataProcessor
from services.forecasting.dataset_builder import DatasetBuilder
from services.sentiment.baseline import SentimentBaselineEngine

logger = logging.getLogger(__name__)


def run() -> None:
    """Run the forecasting pipeline step to build the multimodal dataset."""
    logger.info("Starting forecasting pipeline step")

    tickers = get_watchlist()
    market_processor = MarketDataProcessor(tickers=tickers)
    sentiment_engine = SentimentBaselineEngine()
    dataset_builder = DatasetBuilder(market_processor, sentiment_engine)

    logger.info("Fetching market prices from yfinance")
    prices_df = market_processor.fetch_prices(period="1mo", interval="1d")

    import pandas as pd

    mock_news = pd.DataFrame(
        {
            "title": ["NVDA revenue surge beats expectations"],
            "ticker": ["NVDA"],
            "published_at": [pd.Timestamp.now()],
        }
    )

    logger.info("Building final multimodal dataset")
    dataset = dataset_builder.build_multimodal_dataset(prices_df, mock_news)

    logger.info(f"Dataset creation complete. Total rows: {len(dataset)}")
