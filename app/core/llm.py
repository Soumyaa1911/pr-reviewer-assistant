from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.LLM_API_KEY)


def ask_llm(question: str, context: str = "") -> str:
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content