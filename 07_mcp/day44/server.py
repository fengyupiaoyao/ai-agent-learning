from mcp.server import MCPServer

mcp = MCPServer("ResearchTools")

NOTES = [
    {
        "title": "LangGraph 入门",
        "content": "LangGraph 使用 State、Node 和 Edge 构建工作流。",
    },
    {
        "title": "MCP 架构",
        "content": "MCP 使用标准协议连接 AI 应用与外部能力。",
    },
    {
        "title": "FastAPI 集成",
        "content": "FastAPI 可以将 Agent 封装为 HTTP 服务。",
    },
]


@mcp.tool()
def search_notes(keyword: str) -> list[dict[str, str]]:
    """根据关键词搜索学习笔记。"""
    keyword = keyword.strip()

    if not keyword:
        return ValueError("keyword 不能为空")

    return [
        note
        for note in NOTES
        if keyword.lower() in (
            note["title"] + " " + note["content"]
        ).lower()
    ]


@mcp.resource("research://topics")
def get_topics() -> str:
    """返回当前可用的研究主题。"""
    return "\n".join([note["title"] for note in NOTES])


@mcp.prompt()
def create_research_prompt(topic: str) -> str:
    """生成研究某个主题的提示模板。"""
    return (
        f"请研究以下主题：{topic}\n"
        "请提供核心概念、关键细节、实际示例和待验证的问题。"
    )


if __name__ == "__main__":
    mcp.run()
