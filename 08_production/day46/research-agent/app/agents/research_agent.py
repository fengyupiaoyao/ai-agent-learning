from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from app.core.config import get_settings


def build_research_agent():
    settings = get_settings()

    if not settings.openai_api_key:
        raise ValueError("OpenAI API key is not set")

    model = init_chat_model(
        settings.model_name,
        model_provider="openai",
        temperature=0,
        api_key=settings.openai_api_key,
        base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    )

    return create_agent(
        model=model,
        tools=[],
        system_prompt=(
            "你是一名严谨的研究助手。"
            "请用中文回答，区分已知事实与不确定信息。"
        ),
    )
