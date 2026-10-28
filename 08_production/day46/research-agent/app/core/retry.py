import logging

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

logger = logging.getLogger(__name__)


def retry_transient_call(func):
    return retry(
        retry=retry_if_exception_type(
            (TimeoutError, ConnectionError)
        ),
        wait=wait_random_exponential(
            multiplier=0.5,
            max=4
        )
        stop=stop_after_attempt(3),
        reraise=True,
        before_sleep=lambda state: logger.warning(
            "transient_retry attempt=%s",
            state.attempt_number
        )
    )(func)
