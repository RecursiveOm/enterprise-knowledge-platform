from pydantic import BaseModel

class RetrievalResult(BaseModel):
    chunk_id: str
    content: str
    source: str
    metadata: dict[str, str]
    distance: float