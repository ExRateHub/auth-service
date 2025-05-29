class DomainError(Exception):
    pass


class InvalidHashedPassword(DomainError):
    pass


class InvalidEmail(DomainError):
    pass


class InvalidBase64Encoding(DomainError):
    pass


class InvalidJWTToken(DomainError):
    pass
