import typing

from litestar import Request, Response, status_codes

from application.errors import ApplicationError, AuthenticationError
from domain.errors import DomainError, ValidationError, InvalidCredentialsError
from interface.http.utils.response import make_error_response


def get_exception_handlers_map() -> dict[type[Exception], typing.Callable[[Request, Exception], Response[dict]]]:
    exception_handlers_map = {
        DomainError: domain_error_handler,
        ApplicationError: application_error_handler,
    }
    return exception_handlers_map


def domain_error_handler(request: Request, error: DomainError) -> Response[dict]:
    if isinstance(error, ValidationError):
        return make_error_response(status_code=status_codes.HTTP_400_BAD_REQUEST, details=error.detail)
    elif isinstance(error, InvalidCredentialsError):
        return  make_error_response(status_code=status_codes.HTTP_401_UNAUTHORIZED, details="Invalid login or password")
    return make_error_response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, details="Unexpected application error")


def application_error_handler(request: Request, error: ApplicationError) -> Response[dict]:
    if isinstance(error, AuthenticationError):
        return make_error_response(status_code=status_codes.HTTP_401_UNAUTHORIZED, details=error.detail)
    return make_error_response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, details="Unexpected application error")
