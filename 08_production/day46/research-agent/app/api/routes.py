import logging
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.agent import AgentRequest, AgentResponse
from app.services.research_service import ResearchService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["agent"])


@lru_cache
def get_research_service() -> ResearchService:
    return ResearchService()


@router.post("/run", response_model=AgentResponse)
async def run_agent(
    request: AgentRequest,
    service: ResearchService = Depends(get_research_service)
):
    try:
        answer = await service.run(request.question)
        return AgentResponse(answer=answer)
    except Exception as e:
        logger.exception("Agent 执行失败 | question=%s | error_type=%s", request.question, type(e).__name__)
        raise HTTPException(status_code=500, detail=str(e))
