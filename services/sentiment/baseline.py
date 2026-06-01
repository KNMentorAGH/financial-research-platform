import pandas as pd


class SentimentBaselineEngine:
    """A rule-based sentiment analysis engine for text data.

    This engine evaluates sentiment scores for given text strings or pandas
    DataFrames based on matching tokens against predefined sets of positive
    and negative financial words.
    """

    def __init__(self):  # noqa: D107
        self.positive_words = {"growth", "profit", "surge", "buy", "bullish", "up", "beat"}
        self.negative_words = {"drop", "loss", "fall", "sell", "bearish", "down", "miss"}

    def analyze_text(self, text: str) -> float:
        """Analyzes a single text string and calculates a sentiment score.

        Args:
            text (str): The input text string to be analyzed.

        Returns:
            float: Normalized sentiment score ranging from -1.0 (purely negative)
                to 1.0 (purely positive). Returns 0.0 if no words match or if
                the input is invalid.
        """
        if not isinstance(text, str) or not text:
            return 0.0

        tokens = text.lower().split()
        pos_count = sum(1 for token in tokens if token in self.positive_words)
        neg_count = sum(1 for token in tokens if token in self.negative_words)
        total = pos_count + neg_count

        if total == 0:
            return 0.0

        return (pos_count - neg_count) / total

    def process_news_dataframe(self, df: pd.DataFrame, text_column: str = "title") -> pd.DataFrame:
        """Processes a DataFrame by adding a column with text sentiment scores.

        Args:
            df (pd.DataFrame): Input DataFrame containing text data.
            text_column (str): Name of the column containing the text to analyze.
                Defaults to "title".

        Returns:
            pd.DataFrame: A shallow copy of the input DataFrame with an added
                'Sentiment_Score' column containing float values.
        """
        if df.empty:
            return df

        processed_df = df.copy()
        processed_df["Sentiment_Score"] = processed_df[text_column].apply(self.analyze_text)
        return processed_df
