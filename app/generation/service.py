from app.generation.llm import generate_answer
from app.generation.models import RAGResult
from app.generation.prompt import build_context, build_grounded_prompt
from app.retrieval.retriever import retrieve_documents


NO_INFORMATION_MESSAGE = (
    "I don't have enough information in the company knowledge base "
    "to answer that."
)


def answer_question(
    question: str,
    k: int = 3,
    filters: dict[str, str] | None = None
) -> RAGResult:

    results = retrieve_documents(
        query=question,
        k=k,
        filters=filters
    )

    if not results:
        return RAGResult(
            answer=NO_INFORMATION_MESSAGE,
            sources=[]
        )

    context = build_context(results)

    prompt = build_grounded_prompt(
        question=question,
        context=context
    )

    llm_answer = generate_answer(prompt)

    evidence_map = {}

    for index, result in enumerate(results):
        evidence_id = f"E{index + 1}"
        evidence_map[evidence_id] = result.source

    sources = []

    for evidence_id in llm_answer.evidence_ids:
        source = evidence_map.get(evidence_id)

        if source is not None:
            if source not in sources:
                sources.append(source)

    # Model claimed an answer but selected no valid evidence.
    # Safer to abstain than return an unsupported company answer.
    if not sources:
        return RAGResult(
            answer=NO_INFORMATION_MESSAGE,
            sources=[]
        )

    return RAGResult(
        answer=llm_answer.answer,
        sources=sources
    )