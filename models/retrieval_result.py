from dataclasses import dataclass
from typing import List

from models.chunk import Chunk


@dataclass
class RetrievalResult:
    chunks: List[Chunk]
    retrieval_time_ms: float
