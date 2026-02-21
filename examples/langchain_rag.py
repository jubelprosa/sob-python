"""LangChain RAG pipeline with SOB as retriever.

Install: pip install "sob-python[langchain]" langchain-anthropic
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from sob.integrations.langchain import SOBRetriever

# --- Setup ---

# Free semantic search retriever
retriever = SOBRetriever(mode="search", k=5)

# Premium RAG retriever (full content, requires wallet)
# retriever = SOBRetriever(
#     mode="rag",
#     k=5,
#     premium=True,
#     wallet="YourSolanaWallet...",
# )

# --- RAG Chain ---

prompt = ChatPromptTemplate.from_template(
    """You are a central bank analyst. Answer based on the provided context.

Context:
{context}

Question: {question}

Answer concisely with specific numbers and dates."""
)


def format_docs(docs):
    return "\n\n---\n\n".join(
        f"[{d.metadata.get('institution_code', '?')}] {d.page_content}"
        for d in docs
    )


# To run this example, you need an LLM. Uncomment one:
# from langchain_anthropic import ChatAnthropic
# llm = ChatAnthropic(model="claude-sonnet-4-20250514")

# For testing without an LLM:
print("=== Retrieved Documents ===")
docs = retriever.invoke("ECB interest rate decision 2026")
for doc in docs:
    print(f"\n[{doc.metadata.get('institution_code')}] (sim: {doc.metadata.get('similarity'):.3f})")
    print(doc.page_content[:200])

# Full RAG chain (uncomment llm above):
# chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )
# answer = chain.invoke("What was the latest ECB rate decision?")
# print(answer)
