from core.errors import DetailError


class ApplicationError(DetailError):
    pass

class AuthenticationError(ApplicationError):
    pass

class InvalidTokenError(AuthenticationError):
    detail = "Invalid token."
