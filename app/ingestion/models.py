from pydantic import BaseModel

class SourceDocument(BaseModel):
    content: str
    source: str
    metadata: dict[str, str]

class DocumentChunk(BaseModel):
    chunk_id: str
    content: str
    source: str
    metadata: dict[str, str]