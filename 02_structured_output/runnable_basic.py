from langchain_core.runnables import RunnableLambda


def add_one(x: int) -> int:
    return x + 1


runnable = RunnableLambda(add_one)

result = runnable.invoke(5)

print(result)

chain = (
    RunnableLambda(lambda x: x + 1)
    | RunnableLambda(lambda x: x * 2)
)

result = chain.invoke(5)
print(result)
