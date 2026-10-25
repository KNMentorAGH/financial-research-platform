from fastapi import APIRouter, HTTPException

from services.storage.database import check_connection

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
def health_check() -> dict:
    """Check if the API is running.

    Returns:
        Dictionary with API status.
    """
    return {"status": "ok"}


@router.get("/db")
def database_health_check() -> dict:
    """Check if the API can reach PostgreSQL.

    Returns:
        Dictionary with database status.

    Raises:
        HTTPException: 503 if the database is unreachable.
    """
    if not check_connection():
        raise HTTPException(status_code=503, detail="Database is unreachable")
    return {"status": "ok", "database": "connected"}
