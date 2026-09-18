from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


model = ChatOpenAI(
    model="qwen-plus",
    api_key="sk-ws-H.PDYLPHM.Eqkc.MEUCIHaJSnz5Kwr18ShBxrrW1WJomYmwcjpfVDWkoUBBpf4hAiEAhO_K1GrMAi5CiaJidbznP6a3cGlSkHYjkGJv6jwp1ws",
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一名{role}"
        ),
        (
            "human",
            "{question}"
        ),
    ]
)

# messages = prompt.invoke({
#     "role": "Python 专家",
#     "question": "什么是装饰器？"
# })

# response = model.invoke(messages)

chain = prompt | model

response = chain.invoke({
    "role": "Python 专家",
    "question": "什么是装饰器？"
})

print(response.content)
