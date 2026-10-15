from collections import defaultdict , deque
from app.core.config import settings 

_memory = defaultdict(lambda : deque(maxlen=settings.max_memory_messages))

def add_message(session_id: str, role: str, content: str):
    _memory[session_id].append({"role": role, "content": content})

def get_messages(session_id: str):
    return list(_memory[session_id])    

def build_history(session_id:str):
    return "\n".join(
        f"{item['role']}: {item['content']}"
        for item in get_messages(session_id)
    )

