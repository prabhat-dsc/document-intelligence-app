import logging
from app.core.exceptions import IngestionError
from app.ingestion.pdf_analyzer import analyze_pdf
from app.ingestion.pdf_loader import pdf_loader
from app.ingestion.chunker import chunk_documents
from app.retrieval.vector_store import add_documents
from app.retrieval.hybrid import refresh_keyword_index
from app.services.document_service import update_document, get_document

logger = logging.getLogger(__name__)

def ingest_document(document_id: str, pdf_path: str):
    try:
        record = get_document(document_id)
        if not record:
            raise IngestionError("Document record not found.")

        update_document(document_id, status="PROCESSING")

        analysis = analyze_pdf(pdf_path)

        docs = pdf_loader(
            pdf_path,
            document_id,
            record["filename"],
            analysis["document_type"],
        )

        chunks = chunk_documents(docs)
        add_documents(chunks)
        refresh_keyword_index()

        update_document(
            document_id,
            status="READY",
            pages=analysis["pages"],
            chunks=len(chunks),
        )

        logger.info(
            "ingestion_completed document=%s pages=%s chunks=%s",
            document_id,
            analysis["pages"],
            len(chunks),
        )

    except Exception as exc:
        logger.exception("ingestion_failed document=%s", document_id)
        update_document(
            document_id,
            status="FAILED",
            error=str(exc),
        )
