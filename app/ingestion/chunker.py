
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from app.core.config import settings 


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = settings.chunk_size,
        chunk_overlap = settings.chunk_overlap,
        separators= ["\n\n", "\n", ". "," ", ""]
    )

    chunks = splitter.split_documents(documents)

    for index , chunk in enumerate(chunks):
        chunk.metadata['chunk_id'] = (
            f"{chunk.metadata.get('document_id', 'doc')}_"
            f"{chunk.metadata.get('page','0')}_{index}"
        )


    return chunks


