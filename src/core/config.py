from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict



PROJECT_DIR = Path(__file__).parent.parent.parent.resolve()

class PostgresConnection(BaseSettings):
    name: str
    host: str
    port: int
    username: str
    password: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_DIR / ".env",
        env_file_encoding = "utf-8",
        env_nested_delimiter="_"
    )
    database: PostgresConnection


@lru_cache()
def  get_settings(**kwargs) -> Settings:
    return Settings(**kwargs)