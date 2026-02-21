# sob-python

Python SDK for the [State of Biz (SOB)](https://state-of.biz) central bank intelligence API. Includes LangChain and LlamaIndex integrations for RAG pipelines.

## Install

```bash
pip install sob-python                    # Core client
pip install "sob-python[langchain]"       # + LangChain integration
pip install "sob-python[llamaindex]"      # + LlamaIndex integration
pip install "sob-python[all]"             # Everything
```

## Quick Start

```python
from sob import SOBClient

client = SOBClient()

# Free: list recent items
items = client.list_items(per_page=5)
for item in items.items:
    print(f"[{item.institution_code}] {item.content.headline}")

# Free: semantic search
results = client.search("ECB interest rate decision", limit=5)

# Free: RAG context
rag = client.get_rag_context("What did the ECB decide?", max_tokens=2000)
```

## Premium Access

Premium endpoints require a Solana wallet with credits:

```python
client = SOBClient(wallet="YourSolanaWalletAddress...")

# Tier 1 (1 credit): Metadata
institutions = client.get_institutions()

# Tier 2 (10 credits): Structured data
rates = client.get_rates(institution="ECB")
sentiment = client.get_sentiment(days=7)

# Tier 3 (100 credits): Semantic objects
briefing = client.get_briefing(item_id=12345)
results = client.premium_search("inflation outlook", limit=20)

# Tier 4 (1000 credits): Composite reports
comparison = client.get_cross_institution(["ECB", "FED", "BOE"])
digest = client.get_weekly_digest()
```

### Credit Management

```python
# Check balance
balance = client.get_balance()
print(f"Credits: {balance.balance}")

# Purchase credits (after sending SOL to the x402 wallet)
result = client.purchase_credits(tx_signature="5UfD...")
print(f"New balance: {result.new_balance}")
```

## Async Client

```python
from sob import AsyncSOBClient

async with AsyncSOBClient(wallet="...") as client:
    items = await client.list_items()
    rates = await client.get_rates()
```

## LangChain Integration

```python
from sob.integrations.langchain import SOBRetriever

# Semantic search retriever
retriever = SOBRetriever(mode="search", k=5)
docs = retriever.invoke("ECB rate decision")

# RAG context retriever
retriever = SOBRetriever(mode="rag", k=5)

# Premium (requires wallet)
retriever = SOBRetriever(mode="search", k=10, premium=True, wallet="...")
```

Use in a RAG chain:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
answer = chain.invoke("What was the latest ECB rate decision?")
```

## LlamaIndex Integration

```python
from sob.integrations.llamaindex import SOBReader

# Search mode
reader = SOBReader(mode="search")
docs = reader.load_data(query="ECB rate decision", limit=5)

# Items mode (no query needed)
reader = SOBReader(mode="items")
docs = reader.load_data(institution="ECB", limit=10)

# RAG mode (full content)
reader = SOBReader(mode="rag")
docs = reader.load_data(query="monetary policy", max_tokens=4000)
```

## Error Handling

```python
from sob import SOBClient, PaymentRequired, RateLimited, NotFound

client = SOBClient(wallet="...")

try:
    rates = client.get_rates()
except PaymentRequired as e:
    print(f"Need {e.credits_cost} credits (balance: {e.credits_balance})")
    print(f"Top up wallet: {e.wallet}")
except RateLimited as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except NotFound:
    print("Resource not found")
```

## API Endpoints

| Endpoint | Tier | Credits | Method |
|----------|------|---------|--------|
| `/api/items` | Free | 0 | `list_items()` |
| `/api/item/{slug}` | Free | 0 | `get_item()` |
| `/api/semantic-search` | Free | 0 | `search()` |
| `/api/rag-context` | Free | 0 | `get_rag_context()` |
| `/api/premium/institutions` | 1 | 1 | `get_institutions()` |
| `/api/premium/feed-status` | 1 | 1 | `get_feed_status()` |
| `/api/premium/rates` | 2 | 10 | `get_rates()` |
| `/api/premium/sentiment` | 2 | 10 | `get_sentiment()` |
| `/api/premium/image/{id}` | 2 | 10 | `get_image()` |
| `/api/premium/semantic-search` | 3 | 100 | `premium_search()` |
| `/api/premium/rag-context` | 3 | 100 | `premium_rag_context()` |
| `/api/premium/briefing` | 3 | 100 | `get_briefing()` |
| `/api/premium/image-feed` | 3 | 100 | `get_image_feed()` |
| `/api/premium/cross-institution` | 4 | 1,000 | `get_cross_institution()` |
| `/api/premium/weekly-digest` | 4 | 1,000 | `get_weekly_digest()` |
| `/api/credits/balance` | — | 0 | `get_balance()` |
| `/api/credits/purchase` | — | 0 | `purchase_credits()` |

## Pricing

```
1 SOL = 1,000,000 Credits
Tier 1: 1 credit ($0.00001)
Tier 2: 10 credits ($0.0001)
Tier 3: 100 credits ($0.001)
Tier 4: 1,000 credits ($0.01)
```

## License

MIT
