"""
Core configuration settings for AgriSense AI backend.
Reads configuration from environment variables and .env file safely.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    """Application settings loaded from environment or defaults."""
    
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "default-dev-secret-key-agrisense"
    API_BASE_URL: str = "http://localhost:8000"
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/agrisense_db"
    
    # Fertilizer Module Specific Configuration
    FERTILIZER_MODEL_VERSION: str = "1.0.0"
    FERTILIZER_ARTIFACTS_DIR: str = str(BASE_DIR / "ml" / "artifacts")
    
    # Allowed CORS Origins
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
