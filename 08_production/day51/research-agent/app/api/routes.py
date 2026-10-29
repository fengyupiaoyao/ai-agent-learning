import logging
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, Request

from app.schemas.agent import AgentRequest, AgentResponse
from app.services.research_service import ResearchService

from app.core.rate_limit import RateLimiter

rate_limiter = RateLimiter(
    max_requests=30,
    window_seconds=60,
)


async def enforce_rate_limit(request: Request):
    client = request.client
    key = client.host if client else "unknown"

    if not await rate_limiter.allow(key):
        raise HTTPException(
            status_code=429,
            detail="Too many requests",
            headers={"Retry-After": "60"}
        )


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["agent"])


@lru_cache
def get_research_service() -> ResearchService:
    return ResearchService()


@router.post(
    "/run",
    response_model=AgentResponse,
    dependencies=[Depends(enforce_rate_limit)]
)
async def run_agent(
    request: AgentRequest,
    service: ResearchService = Depends(get_research_service)
):
    answer = await service.run(request.question)
    return AgentResponse(answer=answer)
