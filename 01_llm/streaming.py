from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="qwen-plus",
    api_key="sk-ws-H.PDYLPHM.Eqkc.MEUCIHaJSnz5Kwr18ShBxrrW1WJomYmwcjpfVDWkoUBBpf4hAiEAhO_K1GrMAi5CiaJidbznP6a3cGlSkHYjkGJv6jwp1ws",
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

for chunk in model.stream("介绍一下RAG"):
    print(chunk.content, end="")