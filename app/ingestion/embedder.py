from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def embed_chunks(chunks: list[dict]) -> list[dict]:
    model = get_model()
    texts = [chunk["code"] for chunk in chunks]
    embeddings = model.encode(texts)
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding.tolist()
    return chunks