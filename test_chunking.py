from app.ingestion.repo_loader import clone_repo, get_python_files
from app.ingestion.chunker import chunk_python_file

# A small, simple public repo for testing
repo_url = "https://github.com/psf/requests-html"

print("Cloning repo...")
repo_path = clone_repo(repo_url)
print(f"Cloned to: {repo_path}")

py_files = get_python_files(repo_path)
print(f"Found {len(py_files)} Python files")

# Just chunk the first file as a test
if py_files:
    first_file = py_files[0]
    print(f"\nChunking: {first_file}")
    chunks = chunk_python_file(first_file)
    print(f"Found {len(chunks)} chunks\n")

    for chunk in chunks[:3]:  # show first 3 chunks only
        print(f"--- {chunk['type']}: {chunk['name']} ---")
        print(chunk['code'][:200])  # first 200 chars
        print()

from app.ingestion.embedder import embed_chunks

chunks = embed_chunks(chunks)
print(f"\nFirst chunk embedding (first 5 numbers): {chunks[0]['embedding'][:5]}")
print(f"Embedding length: {len(chunks[0]['embedding'])}")

from app.retrieval.vector_store import add_chunks_to_collection, query_collection

repo_id = "requests-html-test"
add_chunks_to_collection(repo_id, chunks)
print(f"\nStored {len(chunks)} chunks in Chroma collection '{repo_id}'")

# Test a search query
from app.ingestion.embedder import model as embed_model

query_text = "exception for too many retries"
query_embedding = embed_model.encode(query_text).tolist()

results = query_collection(repo_id, query_embedding, n_results=3)

print(f"\nTop matches for query: '{query_text}'")
for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
    print(f"\n--- Match {i+1}: {meta['name']} ({meta['type']}) ---")
    print(doc[:200])