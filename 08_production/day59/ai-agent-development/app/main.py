from fastapi import FastAPI, HTTPException, Request

from contextlib import asynccontextmanager

from app.config import get_settings

from app.observability import request_observability_middleware

from app.metrics import metrics_app

settings = get_settings()

if settings.environment == "production" and settings.debug:
    raise HTTPException(
        status_code=500, detail="Debug mode is disabled in production")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ready = False

    app.state.ready = True

    try:
        yield
    finally:
        app.state.ready = False

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug and settings.environment != "development",
    lifespan=lifespan,
)
app.middleware("http")(request_observability_middleware)

app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    return {"message": "AI Agent API is running"}


@app.get("/health/live")
async def liveness():
    # 只判断应用能否响应，不检查外部模型服务。
    return {"status": "alive"}


@app.get("/health/ready")
async def readiness(request: Request):
    if not getattr(request.app.state, "ready", False):
        raise HTTPException(
            status_code=503,
            detail={"status": "not_ready"},
        )

    return {"status": "ready"}


@app.get("/agent")
async def agent():
    # Day 56 的占位接口，尚未执行真实 Agent 推理。
    return {"message": "Agent endpoint placeholder"}
