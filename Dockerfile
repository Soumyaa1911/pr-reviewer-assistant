FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    pydantic \
    pydantic-settings \
    python-dotenv \
    groq \
    gitpython \
    sentence-transformers \
    chromadb \
    requests \
    langchain \
    langchain-groq \
    langchain-community \
    langchain-huggingface \
    langchain-core \
    langgraph \
    transformers \
    torch

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]