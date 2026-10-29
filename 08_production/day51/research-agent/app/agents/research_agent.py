from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from app.core.config import get_settings


def build_research_agent():
    settings = get_settings()

    if not settings.openai_api_key:
        raise ValueError("OpenAI API key is not set")

    secret = settings.openai_api_key
    model = init_chat_model(
        settings.model_name,
        model_provider="openai",
        temperature=0,
        api_key=secret.get_secret_value(),
        base_url=settings.openai_base_url,
        timeout=settings.request_timeout,
        max_retries=settings.max_retries,
        log_level=settings.log_level,
    )

    return create_agent(
        model=model,
        tools=[],
        system_prompt=(
            "你是一名严谨的研究助手。"
            "请用中文回答，区分已知事实与不确定信息。"
        ),
    )
