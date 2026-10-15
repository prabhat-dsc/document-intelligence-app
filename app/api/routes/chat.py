from fastapi import APIRouter , HTTPException
from app.schemas.chat import ChatRequest , ChatResponse
from app.services.chat_service import chat


router = APIRouter()

@router.post("",response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        return chat(request)
    except Exception as exc:
        raise  HTTPException(status_code=500, detail= str(exc)) 