import pandas as pd
import yfinance as yf


class MarketDataProcessor:
    """Processes and analyzes financial market data.

    This class is designed to handle stock market data for a list of tickers, fetch their
    historical price data, and calculate return metrics. It provides core functionality for
    managing and analyzing financial data over specific time periods and intervals.

    Attributes:
        tickers (list[str]): List of stock ticker symbols for which market data will be
            processed.
    """

    def __init__(self, tickers: list[str]):  # noqa: D107
        self.tickers = tickers

    def fetch_prices(self, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
        """Fetches historical price data for the specified tickers.

        Args:
            period (str): Time period for which data will be fetched.
                Defaults to "1mo" (one month).
            interval (str): Frequency at which data will be returned.
                Defaults to "1d" (daily).

        Returns:
            pd.DataFrame: A DataFrame containing the historical price data for the
                specified tickers, with columns for Date, Open, High, Low, Close,
                Volume, and Ticker.
        """
        combined_data = []
        for ticker in self.tickers:
            ticker_obj = yf.Ticker(ticker)
            df = ticker_obj.history(period=period, interval=interval)
            if df.empty:
                continue
            df = df.reset_index()
            df["Ticker"] = ticker
            combined_data.append(df)

        if not combined_data:
            return pd.DataFrame()

        return pd.concat(combined_data, ignore_index=True)

    @staticmethod
    def calculate_returns(df: pd.DataFrame, target_horizon: int = 1) -> pd.DataFrame:
        """Calculates daily returns and target returns for a given DataFrame.

        Args:
            df (pd.DataFrame): DataFrame of stock price data with columns 'Ticker',
                'Date', and 'Close'.
            target_horizon (int): Integer representing the number of days into the future
                for which to calculate returns. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame with additional columns for 'Daily_Return'
                and 'Target_Return', where 'Daily_Return' is the percentage change in
                closing price from the previous day, and 'Target_Return' is the percentage
                change in closing price from the current day to the day specified by
                target_horizon.
        """
        if df.empty:
            return df

        df = df.sort_values(by=["Ticker", "Date"]).reset_index(drop=True)

        df["Daily_Return"] = df.groupby("Ticker")["Close"].pct_change()

        df["Target_Return"] = df.groupby("Ticker")["Daily_Return"].shift(-target_horizon)

        return df.dropna(subset=["Daily_Return"])
