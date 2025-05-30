import pytest

from core.config import get_settings, Settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()