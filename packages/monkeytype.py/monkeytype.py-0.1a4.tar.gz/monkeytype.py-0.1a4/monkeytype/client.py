import requests
import time
from threading import Lock
from .errors import (
    AuthorizationError,
    RateLimitExceededError,
    ServerError,
    NotFoundError,
    MonkeyTypeException,
)


class Client:
    def __init__(self, api_key: str) -> None:
        self.ape_key = api_key
        self._base_url: str = "http://api.monkeytype.com/"
        self._max_requests_per_minute = 30
        self._tokens = self._max_requests_per_minute
        self._last_refill = time.time()
        self._lock = Lock()

    def _refill(self):
        with self._lock:
            now = time.time()
            elapsed_time = now - self._last_refill
            _tokens_to_add = elapsed_time / 60 * self._max_requests_per_minute
            self._tokens = min(
                self._max_requests_per_minute, self._tokens + _tokens_to_add
            )
            self._last_refill = now

    def _make_request(self, method: str, endpoint: str) -> requests.Response:
        self._refill()

        if self._tokens <= 0:
            raise RateLimitExceededError("You have exceeded the ratelimit.")

        self._tokens -= 1

        headers: dict[str] = {
            "Authorization": f"ApeKey {self.ape_key}",
            "Content-Type": "application/json",
        }

        url: str = self._base_url + endpoint

        try:
            response: requests.Response = requests.request(
                method=method, url=url, headers=headers
            )
        except Exception as e:
            raise e

        possible_errors = {
            401: AuthorizationError,
            470: AuthorizationError,
            471: AuthorizationError,
            404: lambda: NotFoundError("No such username exists."),
            479: RateLimitExceededError,
            429: RateLimitExceededError,
            500: ServerError,
        }

        if response.status_code != 200:
            error_msg = response.json().get("message")
            error = possible_errors.get(response.status_code, MonkeyTypeException)

            if error is MonkeyTypeException:
                raise error(error_msg)
            else:
                raise error()

        return response.json()
