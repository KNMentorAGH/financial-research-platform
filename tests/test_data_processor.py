import pandas as pd
import pytest

from services.forecasting.data_processor import MarketDataProcessor


def test_calculate_returns_empty_dataframe():
    """Test that an empty DataFrame returns gracefully without error."""
    processor = MarketDataProcessor(tickers=["NVDA"])
    df = pd.DataFrame()
    result = processor.calculate_returns(df)
    assert result.empty


def test_calculate_returns_logic():
    """Test if daily returns percentage change is calculated correctly."""
    processor = MarketDataProcessor(tickers=["NVDA"])
    df = pd.DataFrame(
        {
            "Ticker": ["NVDA", "NVDA"],
            "Date": [pd.Timestamp("2026-01-01"), pd.Timestamp("2026-01-02")],
            "Close": [100.0, 110.0],
        }
    )
    result = processor.calculate_returns(df, target_horizon=1)

    assert "Daily_Return" in result.columns
    assert result["Daily_Return"].iloc[0] == pytest.approx(0.1)
