import logging
import sys
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging_config import setup_logging
from app.core.request_context import request_id_var

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logging.info("应用启动")
    yield
    logging.info("应用关闭")


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(router)

logger = logging.getLogger(__name__)


@app.middleware("http")
async def observe_request(request: Request, call_next):
    request_id = uuid.uuid4().hex
    token = request_id_var.set(request_id)
    started = time.perf_counter()

    try:
        logger.info(
            "request_started method=%s path=%s",
            request.method,
            request.url.path,
        )

        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id

        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "request_completed method=%s path=%s "
            "status_code=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response
    except Exception as e:
        logger.exception(
            "request_failed method=%s path=%s",
            request.method,
            request.url.path,
        )
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "request_id": request_id,
            },
            headers={"X-Request-ID": request_id},
        )
    finally:
        request_id_var.reset(token)


@app.get("/health")
async def health():
    return {"status": "ok"}
