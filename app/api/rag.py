from fastapi import APIRouter, HTTPException

from app.generation.service import answer_question
from app.schemas.rag import RAGRequest, RAGResponse


router = APIRouter()


@router.post(
    "/rag",
    response_model=RAGResponse
)
def ask_rag(
    request: RAGRequest
) -> RAGResponse:

    try:
        result = answer_question(
            question=request.question,
            k=request.k,
            filters=request.filters
        )

    except ValueError as error:
        raise HTTPException(
            status_code=500,
            detail="RAG generation failed"
        ) from error

    return RAGResponse(
        answer=result.answer,
        sources=result.sources
    )