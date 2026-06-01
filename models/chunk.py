from dataclasses import dataclass
from models.chunk_metadata import ChunkMetadata

@dataclass
class Chunk:
    id: str
    document_id: str
    text: str
    metadata: ChunkMetadata
