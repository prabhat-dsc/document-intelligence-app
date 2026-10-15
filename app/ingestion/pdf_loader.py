#- This is an important file.
#- It becomes the entry point for PDF ingestion

from PIL import Image
import io 
from langchain_core.documents import Document
import pymupdf
import pytesseract
import logging

from app.core.config import settings
from app.ingestion.ocr import extract_ocr_documents, configure_tesseract
from app.ingestion.image_preprocessor import preprocess_image
from app.ingestion.orientation import detect_orientation, rotate_image


logger = logging.getLogger(__name__)



def pdf_loader(pdf_path: str, document_id: str, filename: str, document_type: str ) -> list[Document]:
    """
    Digital pages use native PDF text.
    Scanned pages use OCR.
    Mixed PDFs are handled page-by-page.
    """
    if document_type == "blank":
        logger.info("Blank Document Skipped : document_id = %s", document_id)
        return []

        
    if document_type == "scanned":
        return extract_ocr_documents(pdf_path, document_id, filename)


    documents = []
    with pymupdf.open(pdf_path) as pdf :
        configure_tesseract()
        for page_no, page in enumerate(pdf,start=1):
            text = page.get_text("text").strip()

            if text :
                documents.append(
                    Document(
                    page_content= text,
                    metadata={
                            "document_id": document_id,
                            "filename": filename,
                            "page": page_no,
                            "loader": "pymupdf",
                            "ocr": False,
                        },
                ))

            else:

                # Simpler fallback: render this page directly.
                
                pix = page.get_pixmap(dpi = settings.ocr_dpi, alpha = False )    
                pil_image = Image.open(io.BytesIO(pix.tobytes("png")))

                processed_image = preprocess_image(pil_image)
                rotation = detect_orientation(processed_image)
                processed_image = rotate_image(processed_image, rotation)

                text = pytesseract.image_to_string(processed_image,
                                                   lang= settings.ocr_language,
                                                   config = "--psm 3"
                                                   ).strip()

                if not text:
                    logger.warning(
                           "No OCR text: document = %s page = %s",
                           document_id, page_no
                    )
                    continue

                documents.append(
                        Document(
                            page_content= text,
                            metadata={
                                "document_id": document_id,
                                "filename": filename,
                                "page": page_no,
                                "loader": "tesseract_ocr",
                                "ocr": True,
                                "rotation": rotation
                            }
                        )
                    )


    return documents







