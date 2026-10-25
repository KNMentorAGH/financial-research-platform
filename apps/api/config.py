from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL


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

    @property
    def database_url(self) -> URL:
        """Build SQLAlchemy connection URL for PostgreSQL.

        Returns:
            SQLAlchemy URL object (password is escaped and hidden when printed).
        """
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )

    class Config:
        """Pydantic config - points to .env file."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
