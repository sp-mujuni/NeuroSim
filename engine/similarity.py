from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class SimilarityScorer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def score(self, query, memories):
        corpus = [m["content"] for m in memories]
        if not corpus:
            return []

        docs = [query] + corpus
        tfidf_matrix = self.vectorizer.fit_transform(docs)
        cosine_scores = cosine_similarity(tfidf_matrix.getrow(0), tfidf_matrix.getrow(1)).flatten()

        scored_memories = [
            {"id": mem["id"], "score": score, "content": mem["content"]}
            for mem, score in zip(memories, cosine_scores)
        ]

        scored_memories.sort(key=lambda x: x["score"], reverse=True)
        return scored_memories[:5]  # return top 5 matches
