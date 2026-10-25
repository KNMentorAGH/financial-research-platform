"""Database schema - SQLAlchemy ORM models for assets, prices and news.

Tables:
    assets       - tracked tickers (seeded from configs/settings.yaml)
    prices       - OHLCV bars, one row per (ticker, date, interval)
    news         - unique news articles (deduplicated by url)
    news_tickers - which tickers an article is related to (many-to-many)
"""

from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# BIGINT autoincrement does not work in SQLite (used in tests) - fall back to INTEGER there.
BigIntPK = BigInteger().with_variant(Integer, "sqlite")


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class Asset(Base):
    """Tracked financial instrument."""

    __tablename__ = "assets"

    ticker: Mapped[str] = mapped_column(String(16), primary_key=True)
    sector: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Price(Base):
    """Single OHLCV price bar for a ticker."""

    __tablename__ = "prices"

    ticker: Mapped[str] = mapped_column(
        String(16), ForeignKey("assets.ticker", ondelete="CASCADE"), primary_key=True
    )
    date: Mapped[date] = mapped_column(Date, primary_key=True)
    interval: Mapped[str] = mapped_column(String(8), primary_key=True, default="1d")

    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False)

    source: Mapped[str] = mapped_column(String(32), nullable=False, default="yfinance")
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class News(Base):
    """Unique news article."""

    __tablename__ = "news"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    publisher: Mapped[str | None] = mapped_column(String(128))
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Sentiment delivered by the data provider (e.g. Alpha Vantage), if any.
    # Model-based sentiment (baseline / FinBERT) is computed by the sentiment service.
    provider_sentiment: Mapped[float | None] = mapped_column(Float)

    source: Mapped[str] = mapped_column(String(32), nullable=False, default="yfinance")
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (Index("ix_news_published_at", "published_at"),)


class NewsTicker(Base):
    """Link between a news article and a related ticker."""

    __tablename__ = "news_tickers"

    news_id: Mapped[int] = mapped_column(
        BigIntPK, ForeignKey("news.id", ondelete="CASCADE"), primary_key=True
    )
    ticker: Mapped[str] = mapped_column(
        String(16), ForeignKey("assets.ticker", ondelete="CASCADE"), primary_key=True
    )

    __table_args__ = (Index("ix_news_tickers_ticker", "ticker"),)
