class DomainError(Exception):
    pass


class InvalidHashedSecret(DomainError):
    pass


class InvalidEmail(DomainError):
    pass


class InvalidBase64Encoding(DomainError):
    pass


class InvalidJWTToken(DomainError):
    pass


class InvalidTTL(DomainError):
    pass
