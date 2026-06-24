from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings
from app.ingestion.pr_loader import get_pr_diff
from app.ingestion.diff_parser import parse_diff

# Shared state between all nodes
class ReviewState(TypedDict):
    repo_id: str
    repo_owner: str
    repo_name: str
    pr_number: int
    diff_text: str
    parsed_files: list
    context: str
    summary: str
    bugs: str
    test_suggestions: str
    final_review: str

# LLM and embeddings
llm = ChatGroq(
    api_key=settings.LLM_API_KEY,
    model_name="llama-3.1-8b-instant",
)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


# Node 1: Fetch and parse the PR diff
def fetch_diff_node(state: ReviewState) -> ReviewState:
    diff_text = get_pr_diff(state["repo_owner"], state["repo_name"], state["pr_number"])
    parsed = parse_diff(diff_text)
    state["diff_text"] = diff_text
    state["parsed_files"] = parsed
    return state


# Node 2: Retrieve related context from vector store
def retrieve_context_node(state: ReviewState) -> ReviewState:
    vectorstore = Chroma(
        collection_name=state["repo_id"],
        embedding_function=embeddings,
        persist_directory=settings.CHROMA_DB_PATH,
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Use added lines as search query
    added_lines = " ".join(
        line for f in state["parsed_files"] for line in f["added"][:5]
    )
    docs = retriever.invoke(added_lines)
    state["context"] = "\n\n".join(doc.page_content for doc in docs)
    return state


# Node 3: Generate a summary of what the PR does
def summarize_node(state: ReviewState) -> ReviewState:
    prompt = f"""Summarize what this PR does in 2-3 sentences.

Diff:
{state['diff_text'][:2000]}"""
    state["summary"] = llm.invoke(prompt).content
    return state


# Node 4: Check for potential bugs
def check_bugs_node(state: ReviewState) -> ReviewState:
    prompt = f"""You are a code reviewer. Based on the diff and codebase context, identify potential bugs or issues.

Context:
{state['context']}

Diff:
{state['diff_text'][:2000]}

List specific potential bugs or issues, or say 'No obvious bugs found.'"""
    state["bugs"] = llm.invoke(prompt).content
    return state


# Node 5: Suggest tests
def suggest_tests_node(state: ReviewState) -> ReviewState:
    prompt = f"""Based on this PR diff, what tests should be added or updated?

Diff:
{state['diff_text'][:2000]}

Be specific about what scenarios need testing."""
    state["test_suggestions"] = llm.invoke(prompt).content
    return state


# Node 6: Combine all findings into final review
def combine_node(state: ReviewState) -> ReviewState:
    state["final_review"] = f"""## PR Review

### Summary
{state['summary']}

### Potential Bugs
{state['bugs']}

### Test Suggestions
{state['test_suggestions']}
"""
    return state


# Build the graph
def build_review_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("fetch_diff", fetch_diff_node)
    graph.add_node("retrieve_context", retrieve_context_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("check_bugs", check_bugs_node)
    graph.add_node("suggest_tests", suggest_tests_node)
    graph.add_node("combine", combine_node)

    graph.set_entry_point("fetch_diff")
    graph.add_edge("fetch_diff", "retrieve_context")
    graph.add_edge("retrieve_context", "summarize")
    graph.add_edge("summarize", "check_bugs")
    graph.add_edge("check_bugs", "suggest_tests")
    graph.add_edge("suggest_tests", "combine")
    graph.add_edge("combine", END)

    return graph.compile()