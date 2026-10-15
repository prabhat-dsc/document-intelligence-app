from pydantic import BaseModel

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    pages: int = 0
    chunks: int = 0
    error: str | None = None
