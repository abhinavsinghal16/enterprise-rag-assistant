from sentence_transformers import SentenceTransformer

from embeddings.embedding_generator import (
    EmbeddingGenerator
)


class SentenceTransformerEmbeddingGenerator(
    EmbeddingGenerator
):

    def __init__(
        self,
        model_name: str = (
            "sentence-transformers/all-MiniLM-L6-v2"
        )
    ):
        self.model = SentenceTransformer(
            model_name
        )

    def generate_embeddings(
        self,
        strings_to_embed: list[str]
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            strings_to_embed,
            normalize_embeddings=True
        )

        return embeddings.tolist()
