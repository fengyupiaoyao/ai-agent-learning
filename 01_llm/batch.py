from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="qwen-plus",
    api_key="sk-ws-H.PDYLPHM.Eqkc.MEUCIHaJSnz5Kwr18ShBxrrW1WJomYmwcjpfVDWkoUBBpf4hAiEAhO_K1GrMAi5CiaJidbznP6a3cGlSkHYjkGJv6jwp1ws",
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

response = model.batch(["介绍一下RAG", "你是谁"])

# response 是一个 list[AIMessage]，逐个解析
for i, msg in enumerate(response):
    print(f"--- 第{i+1}个回答 ---")
    print(f"内容: {msg.content}")                # 文本内容
    print(f"Token用量: {msg.usage_metadata}")     # token 统计
    print()
