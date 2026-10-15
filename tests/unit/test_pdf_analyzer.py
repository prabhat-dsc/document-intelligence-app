from pathlib import Path
import fitz
from app.ingestion.pdf_analyzer import analyze_pdf

def test_digital_pdf_detection(tmp_path: Path):
    path = tmp_path / "test.pdf"

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello world")
    doc.save(path)
    doc.close()

    result = analyze_pdf(str(path))

    assert result["pages"] == 1
    assert result["document_type"] == "digital"

