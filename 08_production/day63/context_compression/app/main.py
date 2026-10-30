from datetime import datetime, timedelta

from app.context_compression import ContextCompressor, ContextItem


def create_demo_data():
    now = datetime.now()

    return [
        ContextItem(
            item_id="1",
            category="goal",
            content="开发一个 Research & Knowledge Agent",
            created_at=now - timedelta(days=5),
        ),
        ContextItem(
            item_id="2",
            category="constraint",
            content="项目必须使用 Python 和 LangGraph",
            created_at=now - timedelta(days=4),
        ),
        ContextItem(
            item_id="3",
            category="fact",
            content="文档检索结果必须提供证据引用",
            created_at=now - timedelta(days=3),
        ),
        ContextItem(
            item_id="4",
            category="background",
            content="之前讨论过项目的目录命名方式",
            created_at=now - timedelta(days=2),
        ),
        ContextItem(
            item_id="5",
            category="noise",
            content="今天讨论了一些无关的普通问题",
            created_at=now - timedelta(days=1),
        ),
        ContextItem(
            item_id="6",
            category="recent",
            content="目前正在开发文档检索模块",
            created_at=now,
        ),
        ContextItem(
            item_id="7",
            category="pending",
            content="下一步需要实现文档引用溯源",
            created_at=now,
        ),
    ]


def main():
    compressor = ContextCompressor()

    items = create_demo_data()

    result = compressor.compress(items, budget=100)

    context = compressor.build_context(result)

    print("=" * 50)
    print("压缩后的 Context")
    print("=" * 50)

    print(context)

    print("\n压缩统计")
    print(f"原始信息数量: {len(items)}")
    print(f"保留信息数量: {len(result.selected)}")
    print(f"删除信息数量: {len(result.dropped)}")
    print(f"估算 Token: {result.estimated_tokens}")
    print(f"Token Budget: {result.budget}")

    print("\n删除的信息")

    for item in result.dropped:
        print(
            f"- [{item.category}] {item.content}"
        )


if __name__ == "__main__":
    main()
