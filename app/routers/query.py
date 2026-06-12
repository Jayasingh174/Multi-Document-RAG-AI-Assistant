from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import embedding_service, vector_service, llm_service
from app.config import TOP_K

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/")
async def ask_question(request: QueryRequest):

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # Create query embedding
        query_embedding = embedding_service.embed_query(request.question)

        # Search FAISS
        results = vector_service.search(query_embedding, k=TOP_K)

        if not results:
            return {
                "answer": "No relevant information found.",
                "sources": []
            }

        # Build context
        context = "\n\n".join(
            [f"[Source: {r.get('source','unknown')}]\n{r.get('text','')}" for r in results]
        )

        if not context.strip():
            return {
                "answer": "No useful information found in retrieved chunks.",
                "sources": []
            }

        # Generate answer
        answer = llm_service.generate_answer(context, request.question)

        # Extract sources
        sources = list({r.get("source", "unknown") for r in results})

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))