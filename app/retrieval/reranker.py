
from app.core.config import settings 
from sentence_transformers import CrossEncoder 

_model =None

def get_ranker():
    global _model 
    if _model is None:
        _model = CrossEncoder(
            model_name = settings.reranker_model
        )
    return _model

def rerank(query: str, documents:list ,top_k: int | None =None):
    if not documents:
        return []
    
    top_k = top_k or settings.rerank_top_k
    pairs = [(query , doc.page_content) for doc in documents]      
    scores = get_ranker().predict(pairs)
    
    ranked = sorted(
        zip(documents, scores),
        key=lambda item: float(item[1]),
        reverse=True,
    )

    return [doc for doc, _ in ranked[:top_k]]

