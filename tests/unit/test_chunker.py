from langchain_core.documents import Document
from app.ingestion.chunker import chunk_documents

def test_chunking_adds_chunk_id():
    docs = [
        Document(
            page_content="A " * 1000,
            metadata={
                "document_id": "doc1",
                "filename": "x.pdf",
                "page": 1,
            },
        )
    ]

    chunks = chunk_documents(docs)

    assert chunks
    assert all("chunk_id" in chunk.metadata for chunk in chunks)

