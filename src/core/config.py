import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from msgspec import field
from pydantic import EmailStr, Field
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


class EmailSMTPConfig(BaseSettings):
    backend: Literal["smtp"]
    host: str = Field(description="SMTP host or API endpoint")
    port: int = Field(default=587, description="SMTP port")
    username: str = Field(description="SMTP username or API key")
    password: str = Field(description="SMTP password or API secret")
    use_tls: bool = Field(default=True, description="Enable STARTTLS")
    use_ssl: bool = Field(default=False, description="Enable SSL/TLS")

class EmailConsoleConfig(BaseSettings):
    backend: Literal["console"]

class EmailSettings(BaseSettings):
    config: EmailSMTPConfig | EmailConsoleConfig
    from_email: EmailStr = Field(description="Default from email address")
    from_name: str | None = Field(default=None, description="Default from name")
    templates_dir: Path = Field(
        default=PROJECT_DIR / "templates" / "emails",
        description="Directory for Jinja2 email templates",
    )

    @property
    def backend(self) -> Literal["console", "smtp"]:
        return self.config.backend

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )
    database: PostgresConnection
    email: EmailSettings


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
