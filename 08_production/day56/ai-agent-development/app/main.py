from fastapi import FastAPI, HTTPException

from contextlib import asynccontextmanager

from app.config import get_settings

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


@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "environment": settings.environment,
        "message": "Welcome to the AI Agent API",
    }


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}


@app.get("/ready")
def ready():
    # 当前版本没有真正连接模型或数据库。
    # 后续需要在这里检查必要依赖是否可用。
    return {
        "status": "ready",
        "checks": {
            "application": "ok",
        },
    }


@app.post("/agent")
def run_agent(question: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question is required")

    return {
        "question": question,
        "message": "Agent integration is not implemented yet",
    }
