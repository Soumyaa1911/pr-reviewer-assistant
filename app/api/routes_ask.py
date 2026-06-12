from fastapi import APIRouter
from app.models.schemas import AskRequest, AskResponse

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    # Placeholder logic - no LLM connected yet
    return AskResponse(
        answer=f"You asked: '{request.question}' about repo '{request.repo_id}'. (LLM not connected yet)",
        sources=[],
    )