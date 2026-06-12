from fastapi import APIRouter
from app.models.schemas import AskRequest, AskResponse
from app.core.llm import ask_llm

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    answer = ask_llm(question=request.question)
    # Placeholder logic - no LLM connected yet
    return AskResponse(
        answer=answer,
        sources=[],
    )