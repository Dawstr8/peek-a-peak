class NotFoundException(Exception):
    """Raised when an expected resource (user) can't be found."""


class ExternalServiceException(Exception):
    """Raised when an external service (API) call fails."""
