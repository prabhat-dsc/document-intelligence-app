
from app.schemas.chat import ChatRequest, ChatResponse, Source
from app.retrieval.hybrid import hybrid_search
from app.retrieval.reranker import rerank
from app.rag.citations import build_context, build_sources
from app.rag.llm import get_llm
from app.rag.memory import add_message, build_history
from app.rag.prompts import RAG_PROMPT

def _rewrite_question(question: str, session_id: str) -> str:
    history = build_history(session_id)
    if not history:
        return question

    # Lightweight context injection for the MVP.
    # The original question is retained so retrieval is not accidentally
    # changed by an aggressive rewrite.
    return f"Conversation context:\n{history}\n\nCurrent question:\n{question}"

def chat(request: ChatRequest):
    query = _rewrite_question(request.question, request.session_id)

    candidates = hybrid_search(
        query,
        document_ids=request.document_ids or None,
    )

    ranked = rerank(query, candidates)

    if not ranked:
        answer = "I don't have enough information in the provided documents."
        add_message(request.session_id, "user", request.question)
        add_message(request.session_id, "assistant", answer)
        return ChatResponse(answer=answer, sources=[])

    context = build_context(ranked)

    prompt_value = RAG_PROMPT.invoke({
        "context": context,
        "question": request.question,
    })

    response = get_llm().invoke(prompt_value)

    answer = response.content
    sources = build_sources(ranked)

    add_message(request.session_id, "user", request.question)
    add_message(request.session_id, "assistant", answer)

    return ChatResponse(
        answer=answer,
        sources=[Source(**source) for source in sources],
    )
