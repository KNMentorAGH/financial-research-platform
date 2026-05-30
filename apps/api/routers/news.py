import yfinance as yf
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/{ticker}")
def get_news(ticker: str) -> dict:
    """Fetch latest news articles for a given ticker.

    Args:
        ticker: Stock ticker symbol (e.g. 'NVDA').

    Returns:
        Dictionary with ticker and list of news articles.

    Raises:
        HTTPException: If news cannot be fetched for the given ticker.
    """
    try:
        stock = yf.Ticker(ticker.upper())
        news = stock.news

        if not news:
            raise HTTPException(
                status_code=404,
                detail=f"No news found for ticker '{ticker.upper()}'",
            )

        articles = []
        for item in news:
            content = item.get("content", {})
            articles.append(
                {
                    "title": content.get("title", ""),
                    "source": content.get("provider", {}).get("displayName", ""),
                    "published_at": content.get("pubDate", ""),
                    "url": (content.get("canonicalUrl") or {}).get("url", ""),
                }
            )

        return {"ticker": ticker.upper(), "count": len(articles), "articles": articles}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch news for '{ticker.upper()}': {e}",
        ) from e
