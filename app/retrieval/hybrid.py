
from app.retrieval.vector_store import get_vector_store
from app.retrieval.bm25 import _bm25
from app.core.config import settings

def refresh_keyword_index():
    # Chroma API is used to rebuild the in-process BM25 index.
    data = get_vector_store().get(include=["documents","metadatas"])
    from langchain_core.documents import Document
    docs = [
        Document(page_content=text, metadata=meta or {})
        for text, meta in zip(data["documents"], data["metadatas"])
    ]
    _bm25.build(docs)


def hybrid_search(query: str, document_ids: list[str] | None = None):
    store =  get_vector_store()

    dense_docs = store.similarity_search(
        query,
        k= settings.dense_top_k,
        filter= (
            {"document_id":{"$in": document_ids}}
            if document_ids else None
        )

    )

    keyword = _bm25.search(query, settings.keyword_top_k) 
    if document_ids:
        allowed = set(document_ids)
        keyword = [
            (doc, score)
            for doc, score in keyword
            if doc.metadata.get("document_id") in allowed
        ]

    # Reciprocal Rank Fusion.
    scores = {}
    docs_by_id = {}

    for rank, doc in enumerate(dense_docs, start=1):
        key = doc.metadata.get("chunk_id", id(doc))
        docs_by_id[key] = doc
        scores[key] = scores.get(key, 0) + 1 / (60 + rank)

    for rank, (doc, _) in enumerate(keyword, start=1):
        key = doc.metadata.get("chunk_id", id(doc))
        docs_by_id[key] = doc
        scores[key] = scores.get(key, 0) + 1 / (60 + rank)

    ranked = sorted(scores, key=scores.get, reverse=True)
    return [docs_by_id[k] for k in ranked]


