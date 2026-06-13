from fastapi import APIRouter
from app.models.schemas import AskRequest, AskResponse
from app.core.llm import ask_llm
from app.ingestion.embedder import model as embed_model
from app.retrieval.vector_store import query_collection

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    # 1. Embed the question
    query_embedding = embed_model.encode(request.question).tolist()

    # 2. Retrieve relevant chunks from the repo's collection
    results = query_collection(request.repo_id, query_embedding, n_results=3)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # 3. Build context string from retrieved chunks
    context = "\n\n".join(
        f"# {meta['name']} ({meta['type']}) in {meta['file']}\n{doc}"
        for doc, meta in zip(documents, metadatas)
    )

    # 4. Ask the LLM with context
    answer = ask_llm(question=request.question, context=context)

    # 5. Build sources list
    sources = [f"{meta['name']} ({meta['file']})" for meta in metadatas]

    return AskResponse(answer=answer, sources=sources)