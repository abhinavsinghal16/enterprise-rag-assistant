from sentence_transformers import CrossEncoder
from models.retrieval_result import RetrievalResult

class Reranker:

    def __init__(self):
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query: str,
        retrieval_result: RetrievalResult,
        top_k: int
    ) -> RetrievalResult:
        pairs = [
            (query, chunk["text"])
            for chunk in retrieval_result.chunks
        ]

        scores = self.model.predict(
            pairs
        )

        scored_chunks = list(
            zip(
                retrieval_result.chunks,
                scores
            )
        )

        scored_chunks.sort(
            key=lambda x: x[1],
            reverse=True
        )

        top_chunks = [
            chunk
            for chunk, score
            in scored_chunks[:top_k]
        ]

        return RetrievalResult(
            chunks=top_chunks,
            retrieval_time_ms=(
                retrieval_result
                .retrieval_time_ms
            )
        )
