from openai import OpenAI
from pydantic import ValidationError

from app.core.config import settings
from app.generation.models import LLMAnswer


def generate_answer(
    prompt: str
) -> LLMAnswer:

    if not settings.llm_api_key:
        raise ValueError("LLM API key is missing")

    client = OpenAI(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url
    )

    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError("LLM returned an empty response")

    try:
        llm_answer = LLMAnswer.model_validate_json(
            content
        )

    except ValidationError as error:
        raise ValueError(
            f"LLM returned invalid structured output: {error}"
        )

    return llm_answer