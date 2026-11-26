from app.services.knowledge_base_service import KnowledgeBaseService

service = KnowledgeBaseService()

# 1. 导入文档
result = service.ingest_file(
    file_path="data/samples/langgraph.txt",
    user_id="user_001",
)

print("导入结果：")
print(result)


# 2. 执行语义检索
results = service.search(
    query="LangGraph 如何保存工作流状态？",
    user_id="user_001",
    k=3,
)

print("\n检索结果：")

for index, document in enumerate(results, start=1):

    print(f"\n排名：{index}")

    print("内容：")
    print(document.page_content)

    print("Metadata：")
    print(document.metadata)
