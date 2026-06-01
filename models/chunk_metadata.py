from dataclasses import dataclass
from typing import Optional

@dataclass
class ChunkMetadata:
    document_name: str
    page: int
    section: Optional[str] = None
