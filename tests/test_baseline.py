import pandas as pd

from services.sentiment.baseline import SentimentBaselineEngine


def test_analyze_text_positive():
    """Test that a text containing only positive words returns a score of 1.0."""
    engine = SentimentBaselineEngine()
    score = engine.analyze_text("growth profit surge")
    assert score == 1.0


def test_analyze_text_negative():
    """Test that a text containing only negative words returns a score of -1.0."""
    engine = SentimentBaselineEngine()
    score = engine.analyze_text("drop loss fall")
    assert score == -1.0


def test_analyze_text_mixed():
    """Test that a text containing equal positive and negative words returns 0.0."""
    engine = SentimentBaselineEngine()
    score = engine.analyze_text("growth drop")
    assert score == 0.0


def test_analyze_text_neutral_or_empty():
    """Test that neutral, empty, or non-string inputs return a score of 0.0."""
    engine = SentimentBaselineEngine()
    assert engine.analyze_text("apple google microsoft") == 0.0
    assert engine.analyze_text("") == 0.0
    assert engine.analyze_text(None) == 0.0


def test_process_news_dataframe():
    """Test that processing a DataFrame adds the correct sentiment scores."""
    engine = SentimentBaselineEngine()
    df = pd.DataFrame(
        {
            "title": [
                "NVDA revenue surge",
                "AMD market share drop",
                "Intel neutral report",
            ]
        }
    )

    result_df = engine.process_news_dataframe(df, text_column="title")

    assert "Sentiment_Score" in result_df.columns
    assert result_df["Sentiment_Score"].iloc[0] > 0.0
    assert result_df["Sentiment_Score"].iloc[1] < 0.0
    assert result_df["Sentiment_Score"].iloc[2] == 0.0


def test_process_news_dataframe_empty():
    """Test that processing an empty DataFrame returns the DataFrame unmodified."""
    engine = SentimentBaselineEngine()
    df = pd.DataFrame()
    result_df = engine.process_news_dataframe(df)
    assert result_df.empty
