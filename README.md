# Document Intelligence RAG

Production-style reference implementation for querying scanned books, research papers, medical reports and other PDFs.

## Architecture

```text
Streamlit
   |
FastAPI
   |
Document Service
   |
PDF Analyzer
   |
Digital text OR OCR
   |
Preprocessing -> Orientation -> OCR
   |
Chunking
   |
Embeddings -> ChromaDB
   |
Hybrid Retrieval (Vector + BM25)
   |
Reranking
   |
Groq LLM
   |
Answer + Page-level Sources
```

## 1. Install

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Tesseract OCR on Windows and update `TESSERACT_CMD` in `.env`.

Copy `.env.example` to `.env` and set your Groq key:

```text
GROQ_API_KEY=...
```

## 2. Start the API

```bash
uvicorn app.main:app --reload
```

API:
`http://localhost:8000`

Swagger:
`http://localhost:8000/docs`

## 3. Start Streamlit

In another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Open:
`http://localhost:8501`

## 4. Workflow

1. Upload one or more PDFs.
2. FastAPI creates a document record.
3. Ingestion runs in the background.
4. Digital PDFs use native PDF text.
5. Scanned pages use OCR.
6. OCR pages are preprocessed and orientation-checked.
7. Text is chunked.
8. Chunks are embedded and stored in ChromaDB.
9. BM25 index is refreshed.
10. Questions use hybrid retrieval.
11. Retrieved candidates are reranked.
12. Groq generates a grounded answer.
13. Sources expose filename and page number.

## 5. Docker

Create `.env`, then:

```bash
docker compose up --build
```

API:
`http://localhost:8000`

Streamlit:
`http://localhost:8501`

## Important production notes

This repository is a production-style **application skeleton/MVP**, not a claim that every component is production-ready for regulated healthcare deployment.

For real deployment add authentication, authorization, tenant isolation, object storage, a durable job queue, PostgreSQL, monitoring, secret management, encryption, retention/deletion policies and security scanning.

For medical documents, keep the product focused on document-grounded retrieval/explanation unless the product has undergone the appropriate clinical, legal, privacy and regulatory review.
