"""Price extraction - downloads OHLCV bars from yfinance into a normalized DataFrame."""

import logging
from datetime import date

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

PRICE_COLUMNS = [
    "ticker",
    "date",
    "interval",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "source",
]


def empty_prices_df() -> pd.DataFrame:
    """Return an empty DataFrame with the normalized price columns.

    Returns:
        Empty DataFrame with PRICE_COLUMNS.
    """
    return pd.DataFrame(columns=PRICE_COLUMNS)


def normalize_history(raw: pd.DataFrame, ticker: str, interval: str) -> pd.DataFrame:
    """Convert raw yfinance history output into the normalized price format.

    Args:
        raw: DataFrame returned by yf.Ticker(...).history(), indexed by Date/Datetime.
        ticker: Ticker symbol the data belongs to.
        interval: Bar interval used for the download (e.g. "1d").

    Returns:
        DataFrame with PRICE_COLUMNS. Dates are calendar dates in the exchange timezone.
    """
    if raw is None or raw.empty:
        return empty_prices_df()

    df = raw.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()
    time_col = "Datetime" if "Datetime" in df.columns else "Date"

    timestamps = pd.to_datetime(df[time_col])
    if timestamps.dt.tz is not None:
        # Keep the exchange-local calendar date (do NOT convert to UTC - it would shift days).
        timestamps = timestamps.dt.tz_localize(None)

    out = pd.DataFrame(
        {
            "ticker": ticker.upper(),
            "date": timestamps.dt.date,
            "interval": interval,
            "open": df["Open"].astype(float),
            "high": df["High"].astype(float),
            "low": df["Low"].astype(float),
            "close": df["Close"].astype(float),
            "volume": df["Volume"],
            "source": "yfinance",
        }
    )
    return out[PRICE_COLUMNS]


def fetch_prices(
    tickers: list[str],
    start: date | None = None,
    period: str = "1y",
    interval: str = "1d",
) -> pd.DataFrame:
    """Download price history for many tickers.

    Prices are adjusted for splits and dividends (yfinance auto_adjust=True),
    so returns calculated from "close" are correct across corporate actions.

    Args:
        tickers: Ticker symbols to download.
        start: First date to download (incremental load). If None, `period` is used.
        period: yfinance period used when `start` is None (e.g. "1y", "5y", "max").
        interval: Bar interval (e.g. "1d").

    Returns:
        Concatenated normalized DataFrame. Tickers that fail are logged and skipped.
    """
    frames = []
    for ticker in tickers:
        try:
            history_kwargs: dict = {"interval": interval, "auto_adjust": True}
            if start is not None:
                history_kwargs["start"] = start.isoformat()
            else:
                history_kwargs["period"] = period

            raw = yf.Ticker(ticker).history(**history_kwargs)
            df = normalize_history(raw, ticker, interval)
            logger.info(f"Fetched {len(df)} price rows for {ticker}")
            if not df.empty:
                frames.append(df)
        except Exception as e:
            logger.warning(f"Failed to fetch prices for {ticker}: {e}")

    if not frames:
        return empty_prices_df()
    return pd.concat(frames, ignore_index=True)
