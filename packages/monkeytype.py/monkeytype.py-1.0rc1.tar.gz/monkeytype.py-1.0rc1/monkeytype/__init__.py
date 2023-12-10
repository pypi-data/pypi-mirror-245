"""
An easy to use python wrapper built around the Monkeytype API. 

Copyright (c) 2023 Maksims K.
License: MIT
"""

from monkeytype.errors import (
    AuthorizationError,
    RateLimitExceededError,
    ServerError,
    MonkeyTypeException,
    NotFoundError,
)
from monkeytype.models.user import User

api_key: str = None

__all__ = [
    "AuthorizationError",
    "RateLimitExceededError",
    "ServerError",
    "MonkeyTypeException",
    "NotFoundError",
    "User",
]
