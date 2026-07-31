# backend/app/core/config/settings.py
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


def find_env_file() -> Path:
    """
    Locate the root .env file.

    Supports local execution and Docker execution.
    """

    current_file = Path(__file__).resolve()

    for parent in current_file.parents:
        env_file = parent / ".env"

        if env_file.exists():
            return env_file

    return Path(".env")


class Settings(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_file=find_env_file(),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Posts Management API"
    app_version: str = "1.0.0"
    app_env: str = "development"

    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    db_host: str = "db"
    db_port: int = 1433
    db_user: str = "sa"
    db_password: str = "YourStrong!Passw0rd"
    db_name: str = "posts_db"

    @property
    def database_url(self) -> str:
        password = quote_plus(self.db_password)

        return (
            f"mssql+pyodbc://{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            "?driver=ODBC+Driver+18+for+SQL+Server"
            "&TrustServerCertificate=yes"
        )


settings = Settings()
