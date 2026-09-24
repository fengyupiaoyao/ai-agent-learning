import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from tools import research_topic
from models import ResearchResult

load_dotenv()

SYSTEM_PROMPT = """
You are an AI research assistant.

Your job is to help users research technical topics.

When external research information is needed,
use the available research tools.

Always provide a concise and structured research result.
"""

model = init_chat_model(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    "openai:qwen3.8-max",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
    extra_body={"enable_thinking": False},
)

agent = create_agent(
    model=model,
    tools=[research_topic],
    system_prompt=SYSTEM_PROMPT,
    response_format=ResearchResult,
)
