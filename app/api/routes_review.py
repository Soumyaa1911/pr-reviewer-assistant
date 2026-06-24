from fastapi import APIRouter
from pydantic import BaseModel
from app.core.review_graph import build_review_graph

router = APIRouter()


class ReviewRequest(BaseModel):
    repo_id: str
    repo_owner: str
    repo_name: str
    pr_number: int


class ReviewResponse(BaseModel):
    review: str
    files_changed: list[str]


@router.post("/review", response_model=ReviewResponse)
def review_pr(request: ReviewRequest):
    # Build and run the graph
    graph = build_review_graph()

    result = graph.invoke({
        "repo_id": request.repo_id,
        "repo_owner": request.repo_owner,
        "repo_name": request.repo_name,
        "pr_number": request.pr_number,
        "diff_text": "",
        "parsed_files": [],
        "context": "",
        "summary": "",
        "bugs": "",
        "test_suggestions": "",
        "final_review": "",
    })

    files_changed = [f["file"] for f in result["parsed_files"]]

    return ReviewResponse(
        review=result["final_review"],
        files_changed=files_changed,
    )