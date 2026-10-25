from datetime import date

import pandas as pd

from services.ingestion import prices
from services.ingestion.prices import PRICE_COLUMNS, fetch_prices, normalize_history


def make_history(start: str = "2026-01-02", days: int = 3) -> pd.DataFrame:
    """Build a DataFrame shaped like yfinance Ticker.history() output."""
    index = pd.date_range(start, periods=days, freq="D", tz="America/New_York", name="Date")
    return pd.DataFrame(
        {
            "Open": [100.0 + i for i in range(days)],
            "High": [105.0 + i for i in range(days)],
            "Low": [95.0 + i for i in range(days)],
            "Close": [102.0 + i for i in range(days)],
            "Volume": [1_000_000 + i for i in range(days)],
            "Dividends": 0.0,
            "Stock Splits": 0.0,
        },
        index=index,
    )


class FakeTicker:
    """Stand-in for yf.Ticker that records history() calls."""

    calls: list[tuple[str, dict]] = []

    def __init__(self, symbol):  # noqa: D107
        self.symbol = symbol

    def history(self, **kwargs):  # noqa: D102
        FakeTicker.calls.append((self.symbol, kwargs))
        if self.symbol == "BROKEN":
            raise RuntimeError("network error")
        if self.symbol == "EMPTY":
            return pd.DataFrame()
        return make_history()


def test_normalize_history_columns_and_dates():
    """Test that raw yfinance output is converted to the normalized format."""
    df = normalize_history(make_history(), "nvda", "1d")

    assert list(df.columns) == PRICE_COLUMNS
    assert df["ticker"].unique().tolist() == ["NVDA"]
    assert df["date"].iloc[0] == date(2026, 1, 2)
    assert df["close"].iloc[0] == 102.0


def test_normalize_history_empty():
    """Test that empty input gives an empty normalized DataFrame."""
    assert normalize_history(pd.DataFrame(), "NVDA", "1d").empty


def test_fetch_prices_skips_failing_tickers(monkeypatch):
    """Test that one failing ticker does not stop the whole download."""
    monkeypatch.setattr(prices.yf, "Ticker", FakeTicker)
    df = fetch_prices(["NVDA", "BROKEN", "EMPTY", "AMD"])

    assert sorted(df["ticker"].unique()) == ["AMD", "NVDA"]
    assert len(df) == 6


def test_fetch_prices_incremental_start(monkeypatch):
    """Test that `start` is passed to yfinance instead of `period`."""
    FakeTicker.calls = []
    monkeypatch.setattr(prices.yf, "Ticker", FakeTicker)
    fetch_prices(["NVDA"], start=date(2026, 1, 2))

    _, kwargs = FakeTicker.calls[0]
    assert kwargs["start"] == "2026-01-02"
    assert "period" not in kwargs
