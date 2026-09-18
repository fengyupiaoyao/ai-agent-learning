from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    """
    你是一名{role}。

    请回答：
    {question}
    """
)
result = prompt.invoke(
    {
        "role": "Python 老师",
        "question": "问题：1+1=？"
    }
)
print(type(result))
