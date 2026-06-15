from fastapi import APIRouter
from pydantic import BaseModel
from app.ingestion.pr_loader import get_pr_diff
from app.ingestion.diff_parser import parse_diff
from app.ingestion.embedder import model as embed_model
from app.retrieval.vector_store import query_collection
from app.prompts.review_prompt import build_review_prompt
from app.core.llm import ask_llm

router = APIRouter()


class ReviewRequest(BaseModel):
    repo_id: str
    repo_owner: str
    repo_name: str
    pr_number: int


class ReviewResponse(BaseModel):
    review: str
    files_changed: list[str]
    sources: list[str]


@router.post("/review", response_model=ReviewResponse)
def review_pr(request: ReviewRequest):
    # 1. Fetch the PR diff
    diff_text = get_pr_diff(request.repo_owner, request.repo_name, request.pr_number)

    # 2. Parse into structured file diffs
    parsed = parse_diff(diff_text)
    files_changed = [f["file"] for f in parsed]

    # 3. Build a search query from added lines
    all_added = " ".join(
        line for f in parsed for line in f["added"][:5]
    )

    # 4. Retrieve related context from indexed codebase
    query_embedding = embed_model.encode(all_added).tolist()
    results = query_collection(request.repo_id, query_embedding, n_results=3)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(
        f"# {meta['name']} ({meta['type']})\n{doc}"
        for doc, meta in zip(documents, metadatas)
    )

    sources = [f"{meta['name']} ({meta['file']})" for meta in metadatas]

    # 5. Build prompt and generate review
    prompt = build_review_prompt(diff=diff_text[:3000], context=context)
    review = ask_llm(question=prompt)

    return ReviewResponse(
        review=review,
        files_changed=files_changed,
        sources=sources,
    )