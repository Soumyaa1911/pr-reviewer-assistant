from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes_ask import router as ask_router
from app.api.routes_index import router as index_router
from app.api.routes_review import router as review_router

app = FastAPI(
    title="PR Reviewer Assistant",
    description="AI assistant that indexes a GitHub repo and answers questions about its code.",
    version="0.1.0",
)

app.include_router(ask_router)
app.include_router(index_router)
app.include_router(review_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")

@app.get("/health")
def health_check():
    return {"status": "ok"}