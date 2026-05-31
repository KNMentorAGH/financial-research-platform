import pandas as pd

from services.forecasting.data_processor import MarketDataProcessor
from services.sentiment.baseline import SentimentBaselineEngine


class DatasetBuilder:
    """Builder for creating multimodal datasets combining market and sentiment data."""

    def __init__(
        self, market_processor: MarketDataProcessor, sentiment_engine: SentimentBaselineEngine
    ):
        """Initialize the dataset builder.

        Args:
            market_processor: Processor handling market price data and returns.
            sentiment_engine: Engine analyzing text sentiment scores.
        """
        self.market_processor = market_processor
        self.sentiment_engine = sentiment_engine

    def aggregate_daily_sentiment(self, news_df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate daily sentiment scores grouped by ticker.

        Args:
            news_df: DataFrame containing raw news articles and publication dates.

        Returns:
            DataFrame with normalized dates, tickers, and calculated mean sentiment.
        """
        if news_df.empty:
            return pd.DataFrame(columns=["Date", "Ticker", "Mean_Sentiment"])

        df_with_sentiment = self.sentiment_engine.process_news_dataframe(news_df)

        df_with_sentiment["Date"] = pd.to_datetime(df_with_sentiment["published_at"]).dt.normalize()

        daily_sentiment = (
            df_with_sentiment.groupby(["Date", "ticker"])["Sentiment_Score"].mean().reset_index()
        )
        daily_sentiment.columns = ["Date", "Ticker", "Mean_Sentiment"]
        return daily_sentiment

    def build_multimodal_dataset(
        self, prices_df: pd.DataFrame, news_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Combine financial data with sentiment analytics into a single dataset.

        Args:
            prices_df: DataFrame containing historical market pricing.
            news_df: DataFrame containing news text context.

        Returns:
            Merged dataset sorted by asset and timeline.
        """
        if prices_df.empty:
            return pd.DataFrame()

        prices_df["Date"] = pd.to_datetime(prices_df["Date"]).dt.normalize()
        prices_with_returns = self.market_processor.calculate_returns(prices_df)

        daily_sentiment = self.aggregate_daily_sentiment(news_df)

        if daily_sentiment.empty:
            dataset = prices_with_returns.copy()
            dataset["Mean_Sentiment"] = 0.0
            return dataset

        daily_sentiment["Date"] = pd.to_datetime(daily_sentiment["Date"]).dt.normalize()

        dataset = pd.merge(prices_with_returns, daily_sentiment, on=["Date", "Ticker"], how="left")

        dataset["Mean_Sentiment"] = dataset["Mean_Sentiment"].fillna(0.0)
        return dataset.sort_values(by=["Ticker", "Date"]).reset_index(drop=True)
