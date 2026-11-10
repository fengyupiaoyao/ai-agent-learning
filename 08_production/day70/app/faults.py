import asyncio


class ToolExecutionError(Exception):
    pass


class FaultPlan:
    def __init__(
        self,
        mode="normal",
        fail_times=0,
    ):
        self.mode = mode
        self.fail_times = fail_times
        self.calls = 0


async def simulated_tool(plan: FaultPlan):
    plan.calls += 1

    if plan.mode == "timeout":
        await asyncio.sleep(1)
    elif plan.mode == "network":
        if plan.calls <= plan.fail_times:
            raise ConnectionError("Network disconnected")
    elif plan.mode == "tool_error":
        raise ToolExecutionError("Tool execution failed")

    return {
        "status": "success",
        "calls": plan.calls,
        "result": "Research completed",
    }
