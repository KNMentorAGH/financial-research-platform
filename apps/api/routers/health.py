from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
def health_check() -> dict:
    """Check if the API is running.

    Returns:
        Dictionary with API status.
    """
    return {"status": "ok"}
