from langchain_core.runnables import RunnableLambda, RunnableParallel

length = RunnableLambda(lambda x: len(x))

upper = RunnableLambda(lambda x: x.upper())

chain = RunnableParallel(length=length, upper=upper)

result = chain.invoke("hello")

print(result)
