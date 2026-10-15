
def build_context(documents):
    blocks = []

    for doc in documents:
        blocks.append(
            f"""
--- SOURCE ---
File: {doc.metadata.get('filename', 'unknown')}
Page: {doc.metadata.get('page', 'unknown')}
Chunk: {doc.metadata.get('chunk_id', 'unknown')}

Content:
{doc.page_content}
"""
        )

    return "\n".join(blocks)

def build_sources(documents):
    return [
        {
            "document_id": doc.metadata.get("document_id", ""),
            "filename": doc.metadata.get("filename", "unknown"),
            "page": int(doc.metadata.get("page", 0)),
            "chunk_id": doc.metadata.get("chunk_id", ""),
        }
        for doc in documents
    ]



