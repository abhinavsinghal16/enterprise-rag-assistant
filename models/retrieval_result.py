from dataclasses import dataclass
from typing import List

from models.chunk import Chunk


@dataclass
class RetrievalResult:
    chunks: List[Chunk]

    candidate_count: int
    reranked_count: int

    retrieval_time_ms: float
