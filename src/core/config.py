import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).parent.parent.parent.resolve()


class PostgresConnection(BaseSettings):
    name: str
    host: str
    port: int
    username: str
    password: str

    engine: str = Field(default="postgresql", frozen=True)
    driver: str = Field(default="psycopg", frozen=True)

    def get_url(self) -> str:
        return f"{self.engine}+{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
    )
    database: PostgresConnection


def _get_env_file() -> Path:
    environment = os.getenv("ENVIRONMENT", default="dev")
    env_file = PROJECT_DIR / f".env.{environment}"
    return env_file


@lru_cache()
def get_settings(**overrides: Any) -> Settings:
    """Return settings"""
    env_file = _get_env_file()
    overrides.setdefault("_env_file", env_file)
    return Settings(**overrides)
