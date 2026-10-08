from langgraph.prebuilt import ToolNode
from tools import add, multiply

tools = [add, multiply]

tool_node = ToolNode(tools=tools)
