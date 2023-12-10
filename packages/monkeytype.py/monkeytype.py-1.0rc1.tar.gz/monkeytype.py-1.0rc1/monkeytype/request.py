import requests
import monkeytype
from monkeytype.errors import (
    AuthorizationError,
    NotFoundError,
    RateLimitExceededError,
    ServerError,
    MonkeyTypeException,
)
from typing import Dict
from ratelimit import limits, RateLimitException


class Request:
    def __init__(self, method: str, endpoint: str):
        self.method = method
        self.endpoint = endpoint
        self.base_url: str = "https://api.monkeytype.com/"

    def execute(self) -> Dict:
        try:
            response = self._make_request()
        except RateLimitException:
            raise RateLimitExceededError(
                "You cannot make more than 30 calls in a minute, slow down."
            )

        possible_errors = {
            401: AuthorizationError,
            470: AuthorizationError,
            471: AuthorizationError,
            472: AuthorizationError,
            404: NotFoundError,
            479: RateLimitExceededError,
            429: RateLimitExceededError,
            500: ServerError,
        }

        if response.status_code != 200:
            error_msg: str = response.json().get("message")
            error = possible_errors.get(response.status_code, MonkeyTypeException)

            raise error(error_msg)

        return response.json()

    @limits(calls=30, period=60)  # Ratelimit set by MonkeyType developers
    def _make_request(self) -> requests.Response:
        headers = self.__headers
        method = self.method
        url = self.base_url + self.endpoint

        try:
            return requests.request(method=method, url=url, headers=headers)
        except requests.HTTPError as e:
            raise e

    @property
    def __headers(self) -> Dict:
        if not monkeytype.api_key:
            raise ValueError("You must provide an API key.")
        return {"Authorization": f"ApeKey {monkeytype.api_key}"}
