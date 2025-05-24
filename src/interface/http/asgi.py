from litestar import Litestar

from src.interface.http.controlles.system import health


def create_asgi_application() -> Litestar:
    """Returned ASGI application.

    :return: ASGI application.
    """
    app = Litestar(
        route_handlers=[
            health,
        ]
    )
    return app
