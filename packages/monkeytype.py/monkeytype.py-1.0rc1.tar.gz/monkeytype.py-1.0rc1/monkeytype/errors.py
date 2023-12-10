class MonkeyTypeException(Exception):
    """Base exception for all exceptions raised by the API wrapper."""

    pass


class AuthorizationError(MonkeyTypeException):
    """Raised for authorization-related errors."""

    pass


class RateLimitExceededError(MonkeyTypeException):
    """Raised when the rate limit for API requests is exceeded."""

    pass


class NotFoundError(MonkeyTypeException):
    """Raised when a requested resource is not found."""

    pass


class ServerError(MonkeyTypeException):
    """Raised for general server errors."""

    pass
