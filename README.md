# PR Reviewer Assistant

An AI-powered assistant that indexes any GitHub repository, answers natural language questions about its codebase, and reviews pull requests using Retrieval-Augmented Generation (RAG).

## How it works

1. **Index a repo** — provide a GitHub URL. The app clones the repo, breaks the code into function/class-level chunks using Python's AST module, generates embeddings for each chunk, and stores them in a vector database (ChromaDB).

2. **Ask questions** — ask anything about the indexed repo. The app embeds your question, retrieves the most relevant code chunks via semantic search, and passes them as context to an LLM (Groq/Llama 3.1) to generate a grounded, source-cited answer.

3. **Review a PR** — provide a PR number. The app fetches the diff from GitHub, retrieves related codebase context, and generates a structured review covering summary, potential issues, suggestions, and test recommendations.

## Tech Stack

- **FastAPI** - REST API framework
- **ChromaDB** - vector database for semantic search
- **sentence-transformers** - local embedding generation (all-MiniLM-L6-v2)
- **Groq (Llama 3.1)** - LLM for answer generation
- **GitPython** - repository cloning
- **Python AST** - code-aware chunking (functions/classes, not arbitrary text splits)
- **GitHub API** - PR diff fetching

## API Endpoints

### POST /repo/index
Clones and indexes a GitHub repository.

Input:
  repo_id: "my-repo"
  repo_url: "https://github.com/user/repo"

### POST /ask
Asks a question about an indexed repo, returns an answer grounded in the actual code with sources.

Input:
  repo_id: "my-repo"
  question: "How does authentication work in this codebase?"

### POST /review
Fetches a GitHub PR diff, retrieves related codebase context, and generates a structured AI code review.

Input:
  repo_id: "my-repo"
  repo_owner: "username"
  repo_name: "repository"
  pr_number: 42

## Setup

1. Clone the repo and navigate into it
2. Create and activate a virtual environment
3. Run: pip install -r requirements.txt
4. Create a .env file with:
   LLM_API_KEY=your_groq_api_key
   GITHUB_TOKEN=your_github_token
   CHROMA_DB_PATH=./data/chroma_db
5. Run: uvicorn app.main:app --reload
6. Visit http://localhost:8000/docs for interactive API docs

## Roadmap

- [x] Code-aware chunking and embedding pipeline
- [x] Semantic search with ChromaDB
- [x] RAG-based Q&A over any repo
- [x] PR/diff review - context-aware code review suggestions
- [ ] Multi-step review agent (LangGraph)
- [ ] Dockerized deployment