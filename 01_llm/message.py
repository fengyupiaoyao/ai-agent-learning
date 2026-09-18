from langchain_openai import ChatOpenAI

from langchain_core.messages import SystemMessage, HumanMessage

model = ChatOpenAI(
    model="qwen-plus",
    api_key="sk-ws-H.PDYLPHM.Eqkc.MEUCIHaJSnz5Kwr18ShBxrrW1WJomYmwcjpfVDWkoUBBpf4hAiEAhO_K1GrMAi5CiaJidbznP6a3cGlSkHYjkGJv6jwp1ws",
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

messages = [
    SystemMessage(content="你是一名专业的Python程序员"),
    HumanMessage(content="什么是装饰器？"),
]

response = model.invoke(messages)
print(response.content)
