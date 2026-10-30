import logging
import time
import uuid

from fastapi import Request

from app.metrics import REQUEST_DURATION, REQUEST_TOTAL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("ai_agent.api")


async def request_observability_middleware(
    request: Request,
    call_next,
):
    request_id = uuid.uuid4().hex
    request.state.request_id = request_id

    started = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        response.headers["X-Request-Id"] = request_id
        return response
    except Exception as e:
        logger.exception(
            "request_failed request_id=%s method=%s path=%s",
            request_id,
            request.method,
            request.url.path,
        )
        raise e
    finally:
        """
        elapsed = time.perf_counter() - started
        logger.info(
            "request_finished request_id=%s method=%s "
            "path=%s status_code=%s duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            status_code,
            elapsed,
        )
        """
        elapsed = time.perf_counter() - started

        route = request.scope.get("route")
        route_name = getattr(route, "path", "unmatched")

        REQUEST_TOTAL.labels(
            method=request.method,
            route=route_name,
            status=str(status_code),
        ).inc()

        REQUEST_DURATION.labels(
            method=request.method,
            route=route_name,
        ).observe(elapsed)

        logger.info(
            "request_finished request_id=%s method=%s "
            "route=%s status_code=%s duration_ms=%.2f",
            request_id,
            request.method,
            route_name,
            status_code,
            elapsed * 1000,
        )
