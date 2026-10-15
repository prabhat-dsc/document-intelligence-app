import fitz 
import warnings
warnings.filterwarnings("ignore")


def analyze_pdf(pdf_path : str) -> dict:
    """ 
    This function is to analyze whether given pdf is 
    digital, scanned or mixed
    """
    with fitz.open(pdf_path) as pdf :
        page_count = len(pdf)

        text_pages = 0
        image_pages = 0
        blank_pages = 0

        for page in pdf :
            text = page.get_text("text").strip()
            images = page.get_images(full=True)

            if text:
                text_pages +=1
            elif images :
                image_pages +=1
            else:
                blank_pages +=1    

    content_pages = page_count - blank_pages

    if content_pages == 0:
        document_type = "blank"

    elif text_pages == content_pages:
        document_type = "digital"

    elif image_pages == content_pages :
        document_type = "scanned" 

    else :
        document_type = "mixed"

    return {
        "pages":page_count,
        "blank_pages" : blank_pages,
        "content_pages":content_pages,
        "text_pages": text_pages,
        "image_pages": image_pages,
        "document_type":document_type
    }   




            

