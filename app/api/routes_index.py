from fastapi import APIRouter
from app.models.schemas import IndexRequest, IndexResponse
from app.ingestion.repo_loader import clone_repo, get_python_files
from app.ingestion.chunker import chunk_python_file
from app.ingestion.embedder import embed_chunks
from app.retrieval.vector_store import add_chunks_to_collection

router = APIRouter()


@router.post("/repo/index", response_model=IndexResponse)
def index_repo(request: IndexRequest):
    repo_path = clone_repo(request.repo_url)
    py_files = get_python_files(repo_path)

    all_chunks = []
    for file_path in py_files:
        chunks = chunk_python_file(file_path)
        all_chunks.extend(chunks)

    if all_chunks:
        all_chunks = embed_chunks(all_chunks)
        add_chunks_to_collection(request.repo_id, all_chunks)

    return IndexResponse(
        message=f"Indexed repo '{request.repo_url}' as '{request.repo_id}'",
        chunks_indexed=len(all_chunks),
    )