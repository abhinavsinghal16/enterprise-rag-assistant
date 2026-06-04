from dataclasses import dataclass
from typing import Optional

@dataclass
class ChunkMetadata:
    document_name: str
    page_number: int
    section: Optional[str] = None
