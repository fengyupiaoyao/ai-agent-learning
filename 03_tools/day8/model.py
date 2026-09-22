import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from tools import calculator
from tools import get_user_name

load_dotenv(".env")

model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

model_with_tools = model.bind_tools([
    calculator,
    get_user_name
])
