import yaml
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/assets", tags=["assets"])


def load_watchlist() -> dict:
    """Load watchlist configuration from settings file.

    Returns:
        Dictionary with sectors and tickers.

    Raises:
        HTTPException: If configuration file cannot be loaded.
    """
    try:
        with open("configs/settings.yaml") as f:
            config = yaml.safe_load(f)
        return config["watchlist"]["sectors"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load watchlist: {e}") from e


@router.get("/recommended")
def get_recommended_assets() -> dict:
    """Return list of recommended assets to track grouped by sector.

    Returns:
        Dictionary with sectors and their tickers.
    """
    sectors = load_watchlist()
    return {"sectors": sectors}


@router.get("/{sector}")
def get_sector_assets(sector: str) -> dict:
    """Return assets for a specific sector.

    Args:
        sector: Sector name (e.g. 'semiconductors').

    Returns:
        Dictionary with tickers for the requested sector.

    Raises:
        HTTPException: If sector is not found in watchlist.
    """
    sectors = load_watchlist()

    if sector not in sectors:
        raise HTTPException(
            status_code=404,
            detail=f"Sector '{sector}' not found. Available: {list(sectors.keys())}",
        )

    return {"sector": sector, "tickers": sectors[sector]["tickers"]}
