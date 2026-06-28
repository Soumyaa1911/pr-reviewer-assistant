from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are an expert code assistant. Use the following code context to answer the question.

Context:
{context}

Question: {question}

Answer:"""
)


def get_rag_chain(repo_id: str):
    llm = ChatGroq(
        api_key=settings.LLM_API_KEY,
        model_name="llama-3.1-8b-instant",
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        collection_name=repo_id,
        embedding_function=embeddings,
        persist_directory=settings.CHROMA_DB_PATH,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )

    return chain, retriever