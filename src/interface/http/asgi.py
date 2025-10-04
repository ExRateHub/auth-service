from dishka import make_async_container
from dishka.integrations.litestar import setup_dishka
from litestar import Litestar
from litestar.logging import StructLoggingConfig
from litestar.openapi import OpenAPIConfig

from core.di import AppProvider
from core.logging import get_logger, setup_logging
from interface.http.controlles.system import health

from interface.http.controlles.auth import AuthController


def create_asgi_application() -> Litestar:
    """Returned ASGI application.

    :return: ASGI application.
    """
    app = Litestar(
        debug=True,
        route_handlers=[
            AuthController,
            health,
        ],
        openapi_config=OpenAPIConfig(title="ExRateHub API", version="1.0.0dev"),
        logging_config=StructLoggingConfig()
    )

    container = make_async_container(AppProvider())

    setup_dishka(container=container, app=app)
    setup_logging()
    return app
