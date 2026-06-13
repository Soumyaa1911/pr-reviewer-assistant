# PR Reviewer Assistant

An AI-powered assistant that indexes any GitHub repository and answers natural language questions about its codebase using Retrieval-Augmented Generation (RAG).

## How it works

1. **Index a repo** — provide a GitHub URL. The app clones the repo, breaks the code into function/class-level chunks using Python's AST module, generates embeddings for each chunk, and stores them in a vector database (ChromaDB).

2. **Ask questions** — ask anything about the indexed repo. The app embeds your question, retrieves the most relevant code chunks via semantic search, and passes them as context to an LLM (Groq/Llama 3.1) to generate a grounded, source-cited answer.

## Tech Stack

- **FastAPI** - REST API framework
- **ChromaDB** - vector database for semantic search
- **sentence-transformers** - local embedding generation (all-MiniLM-L6-v2)
- **Groq (Llama 3.1)** - LLM for answer generation
- **GitPython** - repository cloning
- **Python AST** - code-aware chunking (functions/classes, not arbitrary text splits)

## API Endpoints

### `POST /repo/index`
Clones and indexes a GitHub repository.

```json
{
  "repo_id": "my-repo",
  "repo_url": "https://github.com/user/repo"
}
```

### `POST /ask`
Asks a question about an indexed repo, returns an answer grounded in the actual code with sources.

```json
{
  "repo_id": "my-repo",
  "question": "How does authentication work in this codebase?"
}
```

## Setup

```bash
git clone https://github.com/<your-username>/pr-reviewer-assistant.git
cd pr-reviewer-assistant
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

Create a `.env` file:

LLM_API_KEY=your_groq_api_key
CHROMA_DB_PATH=./data/chroma_db

Run:
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive API documentation.

## Roadmap

- [x] Code-aware chunking and embedding pipeline
- [x] Semantic search with ChromaDB
- [x] RAG-based Q&A over any repo
- [ ] PR/diff review - context-aware code review suggestions
- [ ] Multi-step review agent (LangGraph)
- [ ] Dockerized deployment