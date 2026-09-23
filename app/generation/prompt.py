from app.retrieval.models import RetrievalResult


def build_context(results: list[RetrievalResult]) -> str:
    return "\n\n".join(
        f"[Evidence ID: E{index + 1}]\n[Source: {result.source}]\n{result.content}"
        for index, result in enumerate(results)
    )


def build_grounded_prompt(
    question: str,
    context: str
) -> str:

    prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question using ONLY the provided company context.

Rules:
- Do not use outside knowledge.
- Do not invent company policies or facts.
- Only use evidence IDs that directly support your answer.
- If the context does not contain enough information, say:
  "I don't have enough information in the company knowledge base to answer that."
  and return an empty evidence_ids list.
- Keep the answer concise and factual.

Return ONLY valid JSON in this exact structure:

{{
  "answer": "your answer here",
  "evidence_ids": ["E1"]
}}

Question:
{question}

Context:
{context}
"""

    return prompt.strip()
