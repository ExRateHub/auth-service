from core.errors import DetailError


class DomainError(DetailError):
    """Domain error."""


class ValidationError(DomainError):
    """Validation error."""


class InvalidHashedSecret(ValidationError):
    detail = "Invalid hashed secret."


class InvalidEmail(ValidationError):
    detail = "Invalid email."


class InvalidUsername(ValidationError):
    detail = "Invalid username."


class UsernameAlreadyExists(ValidationError):
    detail = "Username already exists"


class InvalidBase64Encoding(ValidationError):
    detail = "Invalid base 64 encoding."


class InvalidTokenKey(ValidationError):
    detail = "Invalid token key."


class InvalidTTL(ValidationError):
    detail = "Invalid TTL."


class SecurityError(DomainError):
    pass


class InvalidCredentialsError(SecurityError):
    detail = "Invalid credentials."


class TokenExpiredError(SecurityError):
    detail = "Token is expired."


class TokenRevokedError(SecurityError):
    detail = "Token is revoked."