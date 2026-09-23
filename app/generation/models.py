from pydantic import BaseModel


class LLMAnswer(BaseModel):
    answer: str
    evidence_ids: list[str]


class RAGResult(BaseModel):
    answer: str
    sources: list[str]