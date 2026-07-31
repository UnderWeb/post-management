# backend/app/core/config/settings.py

from __future__ import annotations

from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "Posts Management API"
    app_version: str = "1.0.0"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Database
    db_host: str = "localhost"
    db_port: int = 1433
    db_user: str = "sa"
    db_password: str = "YourStrong!Passw0rd"
    db_name: str = "posts_db"

    @property
    def database_url(self) -> str:
        """Build SQLAlchemy connection URL for SQL Server."""

        password = quote_plus(self.db_password)

        return (
            f"mssql+pyodbc://{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            "?driver=ODBC+Driver+18+for+SQL+Server"
            "&TrustServerCertificate=yes"
        )


settings = Settings()
