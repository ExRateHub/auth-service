from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict



PROJECT_DIR = Path(__file__).parent.parent.parent.resolve()
LOGGING_CONFIG = PROJECT_DIR / "logging.yaml"
ENV_FILE = PROJECT_DIR / ".env"


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
        env_file=ENV_FILE, env_file_encoding="utf-8", env_nested_delimiter="_"
    )
    database: PostgresConnection


@lru_cache()
def get_settings(**kwargs) -> Settings:
    """Return settings"""
    return Settings(**kwargs)