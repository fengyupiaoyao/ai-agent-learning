import asyncio
import logging

from app.faults import ToolExecutionError

logger = logging.getLogger(__name__)


async def resilient_call(
    tool,
    timeout=0.1,
    max_retries=2,
    fallback=None,
):
    for attempt in range(max_retries + 1):
        try:
            result = await asyncio.wait_for(
                tool(),
                timeout=timeout,
            )

            logger.info(
                "Tool succeeded: attempt=%s",
                attempt + 1,
            )

            return {
                "status": "success",
                "result": result,
            }
        except (TimeoutError, ConnectionError) as e:
            logger.warning(
                "Transient failure: attempt=%s, error=%s",
                attempt + 1,
                e,
            )
            if attempt == max_retries:
                break
        except ToolExecutionError as e:
            logger.error("Tool execution failed: %s", e)
            break
    logger.warning("Using fallback")

    if fallback is not None:
        return {
            "status": "fallback",
            "data": fallback,
        }

    return {
        "status": "failed",
        "data": None,
    }
