"""LlamaIndex RAG pipeline with SOB as data source.

Install: pip install "sob-python[llamaindex]" llama-index
"""

from sob.integrations.llamaindex import SOBReader

# --- Load Documents ---

# Search mode (default): semantic search
reader = SOBReader(mode="search")
docs = reader.load_data(query="ECB interest rate decision", limit=5)

print(f"=== Search Mode: {len(docs)} documents ===")
for doc in docs:
    print(f"\n[{doc.metadata.get('institution_code')}] (sim: {doc.metadata.get('similarity'):.3f})")
    print(doc.text[:200])

# Items mode: latest items (no query needed)
items_reader = SOBReader(mode="items")
items = items_reader.load_data(institution="ECB", limit=3)

print(f"\n=== Items Mode: {len(items)} documents ===")
for doc in items:
    print(f"  [{doc.metadata.get('institution_code')}] {doc.text[:100]}")

# RAG mode: full content for LLM context
rag_reader = SOBReader(mode="rag")
rag_docs = rag_reader.load_data(query="Federal Reserve monetary policy", max_tokens=2000)

print(f"\n=== RAG Mode: {len(rag_docs)} documents ===")
for doc in rag_docs:
    print(f"  [{doc.metadata.get('institution')}] {doc.text[:150]}")

# --- Build Index (uncomment to use with LlamaIndex query engine) ---

# from llama_index.core import VectorStoreIndex
#
# index = VectorStoreIndex.from_documents(docs)
# query_engine = index.as_query_engine()
# response = query_engine.query("What was the latest ECB rate decision?")
# print(response)
