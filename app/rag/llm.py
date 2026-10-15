
from langchain_groq import ChatGroq 
from app.core.config import settings 

_llm = None 

def get_llm():
    global _llm 

    if _llm is None:
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is not configured.")

    _llm = ChatGroq(
        api_key= settings.groq_api_key ,
        model = settings.groq_model,
        temperature= 0

    )    

    return _llm 
