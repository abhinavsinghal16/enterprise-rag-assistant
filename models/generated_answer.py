from models.source_attribution import (
    SourceAttribution
)


class GeneratedAnswer:

    def __init__(
        self,
        answer: str,
        sources: list[SourceAttribution]
    ):
        self.answer = answer
        self.sources = sources
