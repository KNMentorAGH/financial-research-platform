from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All fields are automatically read from .env file or environment.
    """

    environment: str = "development"

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "financial_research"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    class Config:
        """Pydantic config - points to .env file."""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
