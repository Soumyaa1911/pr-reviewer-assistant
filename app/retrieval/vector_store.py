import chromadb

# Persistent client - stores data on disk in ./data/chroma_db
client = chromadb.PersistentClient(path="./data/chroma_db")


def get_or_create_collection(repo_id: str):
    """Get (or create) a collection for a specific repo."""
    return client.get_or_create_collection(name=repo_id)


def add_chunks_to_collection(repo_id: str, chunks: list[dict]):
    """Store code chunks (with embeddings) in the repo's collection."""
    collection = get_or_create_collection(repo_id)

    ids = [f"{chunk['file']}::{chunk['name']}::{i}" for i, chunk in enumerate(chunks)]
    embeddings = [chunk["embedding"] for chunk in chunks]
    documents = [chunk["code"] for chunk in chunks]
    metadatas = [
        {"name": chunk["name"], "type": chunk["type"], "file": chunk["file"]}
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )


def query_collection(repo_id: str, query_embedding: list[float], n_results: int = 5):
    """Find the most relevant chunks for a query embedding."""
    collection = get_or_create_collection(repo_id)
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )