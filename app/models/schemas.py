from pydantic import BaseModel


class AskRequest(BaseModel):
    repo_id: str
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str] = []

class IndexRequest(BaseModel):
    repo_id: str
    repo_url: str


class IndexResponse(BaseModel):
    message: str
    chunks_indexed: int