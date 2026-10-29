import asyncio
import time


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_seconds: int = 10,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_seconds = recovery_seconds

        self.failures = 0
        self.opened_at = None
        self.half_open = False
        self._lock = asyncio.Lock()

    async def call(self, operation, *args, **kwargs):
        async with self._lock:
            if self.opened_at is not None:
                elapsed = time.monotonic() - self.opened_at

                if elapsed < self.recovery_seconds:
                    raise CircuitOpenError(
                        "Circuit breaker is open. Try again later."
                    )
                if self.half_open:
                    raise CircuitOpenError(
                        "Circuit breaker is half open. Try again."
                    )
                self.half_open = True
        try:
            result = await operation(*args, **kwargs)
        except Exception:
            async with self._lock:
                self.failures += 1
                self.opened_at = time.monotonic()
                self.half_open = False
            raise
        else:
            async with self._lock:
                self.failures = 0
                self.opened_at = None
                self.half_open = False
            return result
