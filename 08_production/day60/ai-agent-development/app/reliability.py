import httpx

from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_random_exponential,
)

import asyncio
import time
from enum import Enum


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerOpen(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 10):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.opened_at = None

        self.lock = asyncio.Lock()
        self.probe_in_progress = False

    async def call(self, func, *args, **kwargs):
        async with self.lock:
            if self.state == CircuitState.OPEN:
                elapsed = time.monotonic() - self.opened_at

                if elapsed < self.recovery_timeout:
                    raise CircuitBreakerOpen(
                        "Circuit breaker is open"
                    )

                self.state = CircuitState.HALF_OPEN

            if self.state == CircuitState.HALF_OPEN:
                if self.probe_in_progress:
                    raise CircuitBreakerOpen(
                        "Recovery probe already running"
                    )
                self.probe_in_progress = True

        try:
            result = await func(*args, **kwargs)

        except Exception:
            async with self.lock:
                self.failure_count += 1

                if (
                    self.state == CircuitState.HALF_OPEN
                    or self.failure_count >= self.failure_threshold
                ):
                    self.state = CircuitState.OPEN
                    self.opened_at = time.monotonic()

                self.probe_in_progress = False

            raise

        else:
            async with self.lock:
                self.failure_count = 0
                self.state = CircuitState.CLOSED
                self.opened_at = None
                self.probe_in_progress = False

            return result


# type: ignore
@retry(
    retry=retry_if_exception(is_retryable_error),
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(multiplier=1, max=10),
    reraise=True,
)
async def call_model_api(
    url: str,
    payload: dict,
) -> dict:
    timeout = httpx.Timeout(
        connect=3.0,
        read=20.0,
        write=10.0,
        pool=5.0
    )
    async with httpx.AsyncClient(
        timeout=timeout,
    ) as client:
        response = await client.post(
            url,
            json=payload,
        )

        response.raise_for_status()

        return response.json()


async def call_model_with_fallback(
    primary_url: str,
    fallback_url: str,
    payload: dict,
) -> dict:
    try:
        result = await call_model_api(
            primary_url,
            payload,
        )
        return {
            "result": result,
            "source": "primary",
            "degraded": False,
        }
    except Exception as exc:
        try:
            result = await call_model_api(
                backup_url,
                payload,
            )
            return {
                "result": result,
                "source": "fallback",
                "degraded": True,
            }
        except Exception as exc:
            return {
                "result": None,
                "source": "fallback_message",
                "degraded": True,
                "message": "Fallback URL also failed",
            }


def is_retryable_error(exc: Exception) -> bool:
    if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
        return True

    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        return status in {429, 500, 502, 503, 504}

    return False
