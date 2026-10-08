from langchain_core.messages import HumanMessage

from graph import graph

from rich import print as pprint


# result = graph.invoke({
#     "messages": [
#         HumanMessage(
#             content="计算 123 * 456"
#         )
#     ],

#     "query": "计算 123 * 456",

#     "tool_results": [],

#     "final_answer": "",
# })


# for message in result["messages"]:
#     print(
#         type(message).__name__,
#         ":",
#         message.content
#     )

for chunk in graph.stream(
    {
        "messages": [
            HumanMessage(
                content="计算 12 + 45, 然后乘以5"
            )
        ],
    },
    stream_mode="updates"
):
    pprint(chunk)
