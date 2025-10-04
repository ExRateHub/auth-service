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


class InvalidJWTToken(ValidationError):
    detail = "Invalid JWT token."


class InvalidTTL(ValidationError):
    detail = "Invalid TTL."
