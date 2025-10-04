import typing

from litestar import Request, Response, status_codes

from application.errors import ApplicationError
from domain.errors import DomainError, ValidationError


def get_exception_handlers_map() -> dict[type[Exception], typing.Callable[[Exception], Response[dict]]]:
    exception_handlers_map = {
        DomainError: domain_error_handler,
        ApplicationError: application_error_handler,
    }
    return exception_handlers_map


def domain_error_handler(request: Request, error: DomainError) -> Response[dict]:
    if isinstance(error, ValidationError):
        content = {
            "status_code": status_codes.HTTP_400_BAD_REQUEST,
            "details": error.detail,
        }
        return Response(
            content=content,
            status_code=status_codes.HTTP_400_BAD_REQUEST,
        )
    raise RuntimeError


def application_error_handler(error: ApplicationError) -> Response[dict]:
    ...