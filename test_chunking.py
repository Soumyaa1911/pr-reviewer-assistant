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