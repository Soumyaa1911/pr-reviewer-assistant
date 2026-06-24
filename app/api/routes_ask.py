from fastapi import APIRouter
from app.models.schemas import AskRequest, AskResponse
from app.core.rag_chain import get_rag_chain

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    chain, retriever = get_rag_chain(request.repo_id)

    # Get source documents
    source_docs = retriever.invoke(request.question)

    # Run the chain
    answer = chain.invoke(request.question)

    sources = [
        f"{doc.metadata.get('name', 'unknown')} ({doc.metadata.get('file', 'unknown')})"
        for doc in source_docs
    ]

    return AskResponse(answer=answer, sources=sources)