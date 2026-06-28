def classify_chunk_complexity(code: str) -> str:
    try:
        from transformers import pipeline
        classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
        )
        result = classifier(code[:512], candidate_labels=["simple", "moderate", "complex"])
        return result["labels"][0]
    except Exception:
        return "unknown"


def classify_chunks(chunks: list[dict]) -> list[dict]:
    for chunk in chunks:
        chunk["complexity"] = classify_chunk_complexity(chunk["code"])
    return chunks