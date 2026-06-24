from transformers import pipeline

# Zero-shot classification pipeline - no fine-tuning needed
# Downloads once (~1.5GB), cached locally after first run
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
)

COMPLEXITY_LABELS = ["simple", "moderate", "complex"]


def classify_chunk_complexity(code: str) -> str:
    """Classify a code chunk as simple, moderate, or complex."""
    # Truncate long chunks to avoid token limits
    truncated = code[:512]

    result = classifier(
        truncated,
        candidate_labels=COMPLEXITY_LABELS,
    )

    # Return the label with highest score
    return result["labels"][0]


def classify_chunks(chunks: list[dict]) -> list[dict]:
    """Add a 'complexity' field to each chunk."""
    for chunk in chunks:
        chunk["complexity"] = classify_chunk_complexity(chunk["code"])
    return chunks