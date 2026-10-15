from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    session_id: str = "default"
    document_ids: list[str] = []

class Source(BaseModel):
    document_id: str
    filename: str
    page: int
    chunk_id: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]