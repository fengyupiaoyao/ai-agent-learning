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
            "你是一名{role}，回答风格为{style}"
        ),
        (
            "human",
            "{question}"
        ),
    ]
)
chain = prompt | model

# response = chain.invoke({
#     "role": "Python 老师",
#     "style": "适合初学者",
#     "question": "什么是asyncio？"
# })
# print(response.content)

# response2 = chain.invoke({
#     "role": "Python 面试官",
#     "style": "面试回答风格",
#     "question": "什么是 asyncio？"
# })

# print(response2.content)

while True:
    question = input("问题: ")
    if question == "exit":
        break

    response = chain.invoke({
        "role": "Python 老师",
        "style": "适合初学者",
        "question": question
    })
    print(response.content)
