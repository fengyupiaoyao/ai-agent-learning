from app.services.document_service import DocumentService

service = DocumentService()

chunks = service.ingest(
    file_path="data/samples/langgraph.txt",
    user_id="user_001",
)

print(f"总 Chunk 数量: {len(chunks)}")

for chunk in chunks:

    print("\n" + "=" * 50)

    print("Content:")
    print(chunk.page_content)

    print("\nMetadata:")
    print(chunk.metadata)
