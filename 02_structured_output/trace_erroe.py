from langchain_core.runnables import RunnableLambda

import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def divide(x):
    return 10 / x


chain = RunnableLambda(divide)


result = chain.invoke(0)

print(result)
