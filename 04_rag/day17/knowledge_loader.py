from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader


def load_documents():
    loader = DirectoryLoader(
        "data",
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )

    return loader.load()


def main():
    documents = load_documents()

    print(
        f"Loaded {len(documents)} documents."
    )

    for i, doc in enumerate(documents):

        print("\n" + "=" * 60)

        print(f"Document #{i}")

        print("\nSource:")
        print(doc.metadata.get("source"))

        print("\nContent:")
        print(doc.page_content[:300])


if __name__ == "__main__":
    main()
