from models.retrieval_result import RetrievalResult
import numpy as np
import time

class SemanticRetriever:

    def __init__(
        self,
        embedding_generator,
        vector_store,
        storage
    ):

        self.embedding_generator = (
            embedding_generator
        )

        self.vector_store = (
            vector_store
        )

        self.storage = storage

    def generate_query_embedding(
        self,
        query: str
    ):

        embeddings = (
           self.embedding_generator
            .generate_embeddings([query])
        )

        return embeddings[0]

    def search(
        self,
        query: str,
        top_k: int = 3
    ):
        start_time = time.perf_counter()
        query_embedding = self.generate_query_embedding(query)
        query_embedding = np.array([query_embedding], dtype=np.float32)

        index = self.vector_store.load_index("data/faiss.index")

        distances, indices = (index.search(query_embedding, top_k))

        embedding_records = (self.storage.load_embeddings())

        chunk_ids = []

        for faiss_position in indices[0]:
            chunk_ids.append(embedding_records[faiss_position]["chunk_id"])

        chunks = (self.storage.load_chunks())

        matching_chunks = []

        for chunk_id in chunk_ids:

            matching_chunk = next(
                chunk
                for chunk in chunks
                if chunk["chunk_id"] == chunk_id
            )

            matching_chunks.append(matching_chunk)

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return RetrievalResult(
            chunks=matching_chunks,
            retrieval_time_ms=elapsed_ms)
