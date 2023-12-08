"""
An easy to use python wrapper built around the Monkeytype API. 

Copyright (c) 2023 Maksims K.
License: MIT
"""

from monkeytype.client import Client
from monkeytype.errors import (
    AuthorizationError,
    RateLimitExceededError,
    ServerError,
    MonkeyTypeException,
    NotFoundError,
)
from monkeytype.models.user import User

__all__ = [
    "Client",
    "AuthorizationError",
    "RateLimitExceededError",
    "ServerError",
    "MonkeyTypeException",
    "NotFoundError",
    "User",
]
