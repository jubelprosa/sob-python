"""Basic usage of the SOB Python SDK."""

from sob import SOBClient

# --- Free Endpoints (no wallet needed) ---

client = SOBClient()

# List recent items
items = client.list_items(per_page=5)
for item in items.items:
    print(f"[{item.institution_code}] {item.content.headline if item.content else item.title}")

# Get a single item
item = client.get_item("ecb-rate-cut-january-2026")
print(f"\nItem: {item.title}")
print(f"Status: {item.status}")

# Semantic search
results = client.search("ECB interest rate decision", limit=3)
for r in results.items:
    print(f"  [{r.similarity:.2f}] {r.headline}")

# RAG context for LLM consumption
rag = client.get_rag_context("What did the ECB decide about rates?", max_tokens=2000)
print(f"\nRAG context: {rag.total_tokens_estimate} tokens, {len(rag.items)} items")

client.close()


# --- Premium Endpoints (wallet with credits required) ---

premium = SOBClient(wallet="YourSolanaWalletAddress...")

try:
    # Tier 1: Metadata
    institutions = premium.get_institutions()
    print(f"\n{institutions.total} institutions tracked")

    # Tier 2: Structured data
    rates = premium.get_rates(institution="ECB")
    for rate in rates.rates:
        print(f"  {rate.label}: {rate.value} ({rate.change})")

    # Tier 3: Full briefing
    briefing = premium.get_briefing(item_id=12345)
    print(f"\nBriefing: {briefing.content.get('headline')}")

    # Tier 4: Cross-institution comparison
    comparison = premium.get_cross_institution(["ECB", "FED", "BOE"], days=7)
    print(f"\nCross-institution: {comparison.total_items} items across {len(comparison.institutions)} banks")

except Exception as e:
    print(f"Premium access failed: {e}")

finally:
    premium.close()
