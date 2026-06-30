# PR Reviewer Assistant

**Live demo:** https://pr-reviewer-assistant.onrender.com
**API docs:** https://pr-reviewer-assistant.onrender.com/docs

An AI-powered assistant that indexes any public GitHub repository, answers natural language questions about its codebase, and generates structured AI code reviews for pull requests — all grounded in the actual source code using Retrieval-Augmented Generation (RAG).

> Note: hosted on Render's free tier. The first request after a period of inactivity may take 30-60 seconds while the server wakes up.

---

## What this project does

Most AI coding tools either dump an entire codebase into a prompt (which breaks down on large repos and produces vague answers) or rely on the model's general training knowledge (which knows nothing about *your* specific code). This project takes a different approach: it reads a real codebase, breaks it into meaningful pieces, stores them so they can be searched by meaning, and only feeds the LLM the specific pieces relevant to each question. The result is answers and reviews grounded in the actual code, not generic guesses.

It does three things:

1. **Indexes a GitHub repository** — clones it, parses every function and class individually, converts each into a vector embedding, and stores it in a vector database.
2. **Answers questions about that codebase** — using semantic search to find relevant code, then an LLM to explain it in plain language with cited sources.
3. **Reviews pull requests** — fetches a PR's diff, retrieves related context from the indexed codebase, and runs it through a multi-step AI agent that produces a structured review (summary, potential bugs, test suggestions).

---

## Tech stack

| Layer | Technology | Purpose |
|---|---|---|
| API framework | **FastAPI** | Serves all endpoints, validates requests/responses |
| Data validation | **Pydantic** | Defines and enforces the shape of every request/response |
| LLM | **Groq (Llama 3.1)** | Generates answers, summaries, and review text |
| Embeddings | **sentence-transformers** (`all-MiniLM-L6-v2`) | Converts code and questions into vectors for semantic search |
| Vector database | **ChromaDB** | Stores and searches code embeddings by meaning |
| Orchestration | **LangChain (LCEL)** | Chains retrieval + prompt + LLM into a single pipeline for `/ask` |
| Agent framework | **LangGraph** | Runs the multi-step PR review as a graph of independent nodes |
| Code parsing | **Python `ast` module** | Splits source files into functions/classes instead of arbitrary text chunks |
| Repo access | **GitPython** | Clones repositories programmatically |
| PR data | **GitHub REST API** | Fetches pull request diffs |
| Classification (optional) | **Hugging Face Transformers** | Zero-shot complexity labeling of code chunks |
| Containerization | **Docker** | Packages the app for consistent, portable deployment |
| Hosting | **Render** | Free-tier cloud deployment with auto-deploy from GitHub |
| Frontend | **HTML / CSS / vanilla JS** | Single-page UI served directly by FastAPI |

---

## How it works — step by step

### 1. Indexing a repository (`POST /repo/index`)

```
GitHub URL → clone locally → walk all .py files
           → parse each file with Python's ast module
           → extract every function/class as a separate "chunk"
           → convert each chunk's code into a 384-dimension embedding
           → store all chunks + embeddings in a ChromaDB collection named after the repo
```

Each repo gets its own isolated collection in ChromaDB, so multiple repos can be indexed without their data mixing.

### 2. Asking a question (`POST /ask`)

```
User's question → embed the question using the same embedding model
                → search the repo's ChromaDB collection for the 3 most similar code chunks
                → format those chunks into a context block
                → send (context + question) to the LLM via a LangChain LCEL pipeline
                → return the LLM's answer + which code chunks were used as sources
```

This is the core RAG loop: retrieve relevant information first, then generate an answer using only that information — rather than relying on the LLM's general knowledge.

### 3. Reviewing a pull request (`POST /review`)

This runs as a **LangGraph** — a graph of six independent steps, each updating a shared state object:

```
[fetch_diff]        → calls the GitHub API, gets the PR's raw diff, parses it into changed files
       ↓
[retrieve_context]  → embeds the added code lines, searches ChromaDB for related existing code
       ↓
[summarize]          → LLM call: "what does this PR do?"
       ↓
[check_bugs]          → LLM call: "given this diff and this related code, what could break?"
       ↓
[suggest_tests]       → LLM call: "what test scenarios does this change need?"
       ↓
[combine]              → merges all three outputs into one structured review
```

Splitting the review into separate focused LLM calls (rather than one large prompt asking for everything at once) produces more detailed and reliable output, because each call has a single, narrow task.

---

## API reference

### `POST /repo/index`
```json
{
  "repo_id": "my-repo",
  "repo_url": "https://github.com/username/repository"
}
```
Returns the number of code chunks indexed.

### `POST /ask`
```json
{
  "repo_id": "my-repo",
  "question": "How does authentication work in this codebase?"
}
```
Returns an answer plus a list of source code chunks used to generate it.

### `POST /review`
```json
{
  "repo_id": "my-repo",
  "repo_owner": "username",
  "repo_name": "repository",
  "pr_number": 42
}
```
Returns a structured review (summary, potential bugs, test suggestions) plus the list of changed files.

Full interactive documentation: `/docs`

---

## Running it locally

```bash
git clone https://github.com/<your-username>/pr-reviewer-assistant.git
cd pr-reviewer-assistant
python -m venv venv
source venv/Scripts/activate      # Windows
pip install -r requirements.txt
```

Create a `.env` file:
```
LLM_API_KEY=your_groq_api_key
GITHUB_TOKEN=your_github_personal_access_token
CHROMA_DB_PATH=./data/chroma_db
```

Run:
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` for the UI, or `http://localhost:8000/docs` for the API documentation.

---

## Running it with Docker

```bash
docker compose up --build
```

The app will be available at `http://localhost:8000`.

---

## Project structure

```
app/
├── main.py                  # FastAPI app, route registration, serves frontend
├── api/
│   ├── routes_index.py      # POST /repo/index
│   ├── routes_ask.py        # POST /ask
│   └── routes_review.py     # POST /review
├── core/
│   ├── config.py            # Environment variable loading (Pydantic Settings)
│   ├── llm.py                # Groq client wrapper
│   ├── rag_chain.py          # LangChain LCEL pipeline for /ask
│   └── review_graph.py       # LangGraph multi-step agent for /review
├── ingestion/
│   ├── repo_loader.py        # Clones repos, finds Python files
│   ├── chunker.py            # AST-based function/class extraction
│   ├── embedder.py           # Generates embeddings via sentence-transformers
│   ├── pr_loader.py          # Fetches PR diffs from GitHub API
│   ├── diff_parser.py        # Parses raw diffs into structured file changes
│   └── classifier.py         # Optional zero-shot complexity classification
├── retrieval/
│   └── vector_store.py       # ChromaDB collection management and querying
├── models/
│   └── schemas.py            # Pydantic request/response models
└── static/
    └── index.html             # Frontend UI

Dockerfile
docker-compose.yml
render.yaml
```

---

## Why these design decisions

**Why chunk by function/class instead of fixed-size text blocks?** Code has natural structural boundaries. Splitting at function/class level (via the `ast` module) keeps each chunk semantically complete and meaningful on its own, rather than cutting a function in half mid-logic the way fixed-length splitting would.

**Why a separate ChromaDB collection per repo?** Keeps each repo's code isolated, so a question about one repo never accidentally retrieves code from a different one.

**Why LangGraph for reviews but plain LangChain for Q&A?** `/ask` is a single retrieve-then-generate operation, which LCEL handles cleanly in one pipeline. PR review is a multi-faceted task (summary, bugs, tests are different concerns), so splitting it into independent graph nodes produces more focused, detailed output than asking one LLM call to do everything at once.

**Why Groq over OpenAI?** Free tier with fast inference, suitable for a student project without ongoing API costs.

---

## Roadmap

- [x] Code-aware chunking and embedding pipeline
- [x] Semantic search with ChromaDB
- [x] RAG-based Q&A over any public repo
- [x] PR/diff review with codebase-grounded context
- [x] LangChain LCEL refactor
- [x] Multi-step review agent (LangGraph)
- [x] Dockerized deployment
- [x] Live cloud deployment (Render)
- [x] Web frontend
- [ ] Support for languages beyond Python
- [ ] Authentication and per-user repo limits
