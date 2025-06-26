import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@db:5432/app"
    )
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:8080"
    ]

    class Config:
        env_file = ".env"


settings = Settings()