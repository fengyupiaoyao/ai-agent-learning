from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="qwen-plus",
    api_key="sk-ws-H.PDYLPHM.Eqkc.MEUCIHaJSnz5Kwr18ShBxrrW1WJomYmwcjpfVDWkoUBBpf4hAiEAhO_K1GrMAi5CiaJidbznP6a3cGlSkHYjkGJv6jwp1ws",
    base_url="https://ws-wopagvlf3afu5baf.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

while True:
    user_input = input("User: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    print("AI: ", end="")

    for chunk in model.stream(user_input):
        print(chunk.content, end="", flush=True)

    print()
