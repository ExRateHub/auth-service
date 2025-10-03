from litestar import Litestar

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
        ]
    )
    return app
