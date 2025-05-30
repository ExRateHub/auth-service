class DomainError(Exception):
    pass


class InvalidHashedSecret(DomainError):
    pass


class InvalidEmail(DomainError):
    pass


class InvalidBase64Encoding(DomainError):
    pass


class InvalidJwtHeader(DomainError):
    pass


class InvalidJwtPayload(DomainError):
    pass


class InvalidJwtToken(DomainError):
    pass


class InvalidTTL(DomainError):
    pass
