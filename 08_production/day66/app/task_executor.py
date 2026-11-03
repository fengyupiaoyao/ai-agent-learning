from app.idempotency import generate_request_hash

class TaskExecutor:
    def __init__(self, repository, agent):
        self.repository = repository
        self.agent = agent

    async def execute(
            self,
            user_id,
            idempotency_key,
            prompt,
    ):
        request_hash = generate_request_hash({
            "prompt": prompt,
        })

        task, created = self.repository.create_or_get(
            user_id=user_id,
            idempotency_key=idempotency_key,
            request_hash=request_hash,
        )

        if not created:
            if task["status"] == "succeeded":
                return {
                    "task_id": task["id"],
                    "status": "succeeded",
                    "result": task["result"],
                    "duplicate": True,
                }
            return {
                "task_id": task["id"],
                "status": task["status"],
                "result": None,
                "duplicate": False,
            }
        task_id = task["id"]

        self.repository.update_status(
            task_id=task_id,
            status="running",
        )

        try:
            result = await self.agent.run(prompt)

            self.repository.update_status(
                task_id=task_id,
                status="succeeded",
                result=str(result),
            )

            return {
                "task_id": task_id,
                "status": "succeeded",
                "result": result,
                "duplicate": False,
            }
        except Exception as exc:

            self.repository.update_status(
                task_id=task_id,
                status="failed",
                error=str(exc),
            )

            raise
