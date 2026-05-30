from fastapi import FastAPI

from apps.api.routers import assets, health, news


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Financial Research Platform",
        description="Research platform for analyzing the impact of news on stock market behavior.",
        version="0.1.0",
    )

    app.include_router(health.router)
    app.include_router(assets.router)
    app.include_router(news.router)

    return app


app = create_app()
