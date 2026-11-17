from app.contracts import HandoffEnvelope


class HandoffError(Exception):
    pass


ALLOWED_HANDOFFS = {
    "researcher": {"analyst"},
    "analyst": {"reviewer"},
    "reviewer": set(),
}


def create_handoff(
    task_id: str,
    from_agent: str,
    to_agent: str,
    payload: dict,
    context_summary: str = "",
    artifacts: list[str] | None = None,
) -> HandoffEnvelope:
    if from_agent not in ALLOWED_HANDOFFS:
        raise HandoffError(f"Handoff from {from_agent} is not allowed")

    if to_agent not in ALLOWED_HANDOFFS[from_agent]:
        raise HandoffError(
            f"Handoff from {from_agent} to {to_agent} is not allowed")

    if not task_id.strip():
        raise HandoffError("Task ID cannot be empty")

    if not payload:
        raise HandoffError("Payload cannot be empty")

    return HandoffEnvelope(
        task_id=task_id,
        from_agent=from_agent,
        to_agent=to_agent,
        payload=payload,
        context_summary=context_summary,
        artifacts=artifacts or [],
    )


def accept_handoff(
    handoff: HandoffEnvelope,
    receiver: str,
) -> HandoffEnvelope:
    if handoff.to_agent != receiver:
        raise HandoffError(f"Handoff is not for {receiver}")

    if handoff.status != "pending":
        raise HandoffError(f"Handoff is not pending")

    return handoff.model_copy(
        update={"status": "accepted"}
    )


def reject_handoff(
    handoff: HandoffEnvelope,
    receiver: str,
) -> HandoffEnvelope:
    if handoff.to_agent != receiver:
        raise HandoffError(f"Handoff is not for {receiver}")

    if handoff.status != "pending":
        raise HandoffError(f"Handoff is not pending")

    return handoff.model_copy(
        update={"status": "rejected"}
    )
