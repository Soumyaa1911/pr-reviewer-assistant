from fastapi import FastAPI
from app.api.routes_ask import router as ask_router
from app.api.routes_index import router as index_router

app = FastAPI(
    title="PR Reviewer Assistant",
    description="AI assistant that indexes a GitHub repo and answers questions about its code.",
    version="0.1.0",
)

app.include_router(ask_router)
app.include_router(index_router)

@app.get("/")
def root():
    return {"message": "PR Reviewer Assistant is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}