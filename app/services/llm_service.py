import ollama
from app.config import (
    OLLAMA_MODEL,
    OLLAMA_TEMPERATURE,
    OLLAMA_MAX_TOKENS
)


def generate_answer(context: str, question: str) -> str:
    """
    Generate answer using Ollama LLM.
    Answers strictly from provided context.
    """

    if not context or not context.strip():
        return "Information not available in uploaded documents."

    prompt = f"""
Context:
{context}

Question:
{question}

Answer using ONLY the context above.
If the answer is not present in the context, reply exactly:
Information not available in uploaded documents.
"""

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise document analysis assistant that answers only using provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": OLLAMA_TEMPERATURE,
                "num_predict": OLLAMA_MAX_TOKENS
            }
        )

        return response["message"]["content"].strip()

    except Exception as e:
        return f"LLM Error: {str(e)}"