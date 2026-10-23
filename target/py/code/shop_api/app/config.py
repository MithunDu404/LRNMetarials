"""Settings: every value the app needs from the outside world, read once.

pydantic-settings reads environment variables (and a .env file if present),
validates their types, and fails at startup if something is wrong -- not at
3 a.m. on the first request that needs the value.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # SHOP_DATABASE_URL=... in the environment overrides the default below.
    model_config = SettingsConfigDict(env_file=".env", env_prefix="SHOP_")

    database_url: str = "sqlite+aiosqlite:///./shop.db"
    jwt_secret: str = "dev-only-secret-change-me-in-production-0123456789"  # a real deployment injects a long random secret
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:5173"]


@lru_cache  # build the Settings object once per process, then reuse it
def get_settings() -> Settings:
    return Settings()
