
from langchain_chroma import Chroma 
from app.retrieval.embeddings import get_embeddings
from app.core.config import settings

_vector_store = None

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        settings.chroma_dir.mkdir(parents=True, exist_ok=True)

        _vector_store = Chroma(
            collection_name= "document_chunks",
            embedding_function= get_embeddings(),
            persist_directory= str(settings.chroma_dir)
        )
    return _vector_store    

def add_documents(chunks):
    if chunks:
        get_vector_store().add_documents(chunks)

def delete_document_chunks(document_id: str):
    store = get_vector_store()
    store.delete(where = {"document_id": document_id})
