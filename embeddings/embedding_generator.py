from abc import ABC, abstractmethod


class EmbeddingGenerator(ABC):

    @abstractmethod
    def generate_embeddings(
        self,
        strings_to_embed: list[str]
    ) -> list[list[float]]:
        pass
