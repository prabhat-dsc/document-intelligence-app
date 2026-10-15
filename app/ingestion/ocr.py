
import io 
import logging 
from  PIL  import Image
import pytesseract 
import fitz 
import warnings 
warnings.filterwarnings("ignore")
from langchain_core.documents import Document 

from app.core.config import settings 
from app.ingestion.image_preprocessor import preprocess_image
from app.ingestion.orientation import detect_orientation ,rotate_image


logger = logging.getLogger(__name__)

def configure_tesseract():
    if settings.tesseract_cmd :
       pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd
   
def extract_ocr_documents(pdf_path :str, document_id: str, filename:str) ->list[Document]:
    configure_tesseract()

    documents = []

    with fitz.open(pdf_path) as pdf :
      for page_no, page in enumerate(pdf, start=1):
        pix = page.get_pixmap(dpi = settings.ocr_dpi ,alpha =False)
        image = Image.open(io.BytesIO(pix.tobytes("png")))

        processed = preprocess_image(image)
        rotation = detect_orientation(processed)
        processed= rotate_image(processed ,rotation)

        text = pytesseract.image_to_string(
           processed ,
           lang = settings.ocr_language,
           config= "--psm 3"     ## Page Segmentation Mode for pagelout
        ).strip()

        if not text:
                logger.warning(
                    "No OCR text: document=%s page=%s",
                    document_id, page_no
                )
                continue

           
        document = Document(
              page_content= text,
              metadata = {
                   "document_id": document_id,
                        "filename": filename,
                        "page": page_no,
                        "loader": "tesseract_ocr",
                        "rotation": rotation,
                        "ocr": True,
              }
           )
        documents.append(document)

    return documents      



