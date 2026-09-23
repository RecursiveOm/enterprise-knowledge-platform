from pydantic import BaseModel, Field


class RAGRequest(BaseModel):
    question: str = Field(min_length=1)
    k: int = Field(default=3, ge=1)
    filters: dict[str, str] | None = None


class RAGResponse(BaseModel):
    answer: str
    sources: list[str]
