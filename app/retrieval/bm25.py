from rank_bm25 import BM25Okapi

class BM25Index:
    def __init__(self):
        self.documents = []
        self.model = None

    def build(self, documents):
        self.documents = documents 

        tokenized = [
            doc.page_content.lower().split()
              for doc in documents
        ]    

        self.model = BM25Okapi(tokenized) if tokenized else None

    def search(self, query: str , k: int =20):
        if self.model is None:
            return []
        scores =   self.model.get_scores(query.lower().split()) 
        indices = sorted(range(len(scores)), key =lambda i : scores[i], reverse=True)[:k]

        return [(self.documents[i], float(scores[i])) for i in indices]

_bm25 =  BM25Index()   

