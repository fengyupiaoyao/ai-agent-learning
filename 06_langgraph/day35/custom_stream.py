from langgraph.config import get_stream_writer


def search_node(state):

    writer = get_stream_writer()

    writer({
        "type": "status",
        "message": "正在搜索知识库..."
    })

    # 模拟搜索
    docs = [
        "LangGraph 是一个 Agent 工作流框架",
        "LangGraph 支持 State",
        "LangGraph 支持 Checkpoint"
    ]

    writer({
        "type": "status",
        "message": f"找到 {len(docs)} 个文档"
    })

    return {
        "documents": docs
    }
