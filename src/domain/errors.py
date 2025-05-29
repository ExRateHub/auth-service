class DomainError(Exception):
    pass


class InvalidHashedPassword(DomainError):
    pass

class InvalidEmail(DomainError):
    pass
