"""Shared test fixtures using httpx MockTransport."""

import json

import httpx
import pytest

# Sample response data used across tests
SAMPLE_ITEM = {
    "id": 12345,
    "slug": "ecb-rate-cut-january-2026",
    "url": "https://ecb.europa.eu/press/pr/date/2026/html/ecb.mp260108.en.html",
    "title": "ECB announces interest rate decision",
    "institution_code": "ECB",
    "institution_name": "European Central Bank",
    "status": "published",
    "published_at": "2026-01-08T14:00:00",
    "enriched_at": "2026-01-08T14:05:00",
    "content": {
        "headline": "ECB cuts interest rate to 2.75 percent",
        "lead": "The ECB has reduced its key rate by 25bp to 2.75%.",
        "body": None,
        "quote": None,
        "key_facts": [{"label": "New Rate", "value": "2.75%", "change": "-0.25pp"}],
    },
    "classification": {
        "category": "Press",
        "communication_type": "policy_decision",
        "content_density": "standard",
        "policy_areas": ["monetary_policy", "interest_rates"],
    },
    "source_url": None,
    "processed_at": None,
    "processing": None,
    "document": None,
    "next_event": None,
}

SAMPLE_SEARCH_RESPONSE = {
    "query": "ECB interest rate",
    "items": [
        {
            "id": 12345,
            "slug": "ecb-rate-cut-january-2026",
            "url": "https://ecb.europa.eu/...",
            "title": "ECB announces rate decision",
            "headline": "ECB cuts rate to 2.75%",
            "lead": "The ECB has reduced its key rate by 25bp.",
            "institution_code": "ECB",
            "institution_name": "European Central Bank",
            "similarity": 0.9234,
            "published_at": "2026-01-08T14:00:00",
        }
    ],
    "total": 1,
}

SAMPLE_RAG_RESPONSE = {
    "query": "ECB monetary policy",
    "items": [
        {
            "id": 12345,
            "headline": "ECB cuts rate to 2.75%",
            "lead": "The ECB has reduced its key rate.",
            "body_text": "Full text of the ECB decision...",
            "institution": "European Central Bank",
            "published_at": "2026-01-08",
            "source_url": "https://ecb.europa.eu/...",
            "similarity": 0.9234,
        }
    ],
    "total_tokens_estimate": 500,
}

SAMPLE_BALANCE = {
    "wallet": "TestWallet123456789012345678901234",
    "balance": 850,
    "total_purchased": 1000,
    "total_spent": 150,
}

SAMPLE_INSTITUTIONS = {
    "institutions": [
        {
            "code": "ECB",
            "name": "European Central Bank",
            "active": True,
            "total_items": 1234,
            "published_items": 1100,
            "failed_items": 12,
            "latest_item_at": "2026-02-15T14:30:00",
        }
    ],
    "total": 1,
}

SAMPLE_RATES = {
    "rates": [
        {
            "institution": "ECB",
            "institution_name": "European Central Bank",
            "label": "Deposit Rate",
            "value": "2.75%",
            "change": "-0.25pp",
            "source_date": "2026-02-10T14:00:00",
        }
    ],
    "total": 1,
}

SAMPLE_SENTIMENT = {
    "sentiments": [
        {
            "institution": "FED",
            "institution_name": "Federal Reserve",
            "category": "Speech",
            "communication_type": "policy_guidance",
            "policy_areas": ["monetary_policy"],
            "headline": "Powell: Inflation progress continues",
            "published_at": "2026-02-14T18:00:00",
        }
    ],
    "total": 1,
    "period_days": 7,
}

SAMPLE_BRIEFING = {
    "id": 12345,
    "slug": "ecb-rate-cut",
    "url": "https://ecb.europa.eu/...",
    "title": "ECB rate decision",
    "institution_code": "ECB",
    "institution_name": "European Central Bank",
    "published_at": "2026-01-08T14:00:00",
    "content": {"headline": "ECB cuts rate", "lead": "..."},
    "classification": {"category": "Press"},
    "temporal": {},
    "extraction": {"pages": 2},
    "processing": {"model": "gemini-2.5-flash"},
}

SAMPLE_CROSS_INSTITUTION = {
    "institutions": [
        {
            "institution_code": "ECB",
            "institution_name": "European Central Bank",
            "items": [{"id": 1, "headline": "ECB rate cut"}],
        }
    ],
    "period_days": 7,
    "total_items": 1,
}

SAMPLE_WEEKLY_DIGEST = {
    "period": "7 days",
    "total_items": 1,
    "by_category": {"Press": [{"id": 1, "headline": "ECB rate cut"}]},
    "by_institution": {"ECB": [{"id": 1, "headline": "ECB rate cut"}]},
}

SAMPLE_FEED_STATUS = {
    "daily_stats": [{"day": "2026-02-15", "items": 47, "institutions": 18}],
    "pipeline_status": {"published": 12500, "enriched": 200},
}

SAMPLE_IMAGE_METADATA = {
    "item_id": 12345,
    "headline": "ECB rate cut",
    "institution_code": "ECB",
    "image_prompt": None,
    "generated_at": None,
    "formats": [
        {"format": "hero", "width": 1280, "height": 720, "url": "https://cms.state-of.biz/assets/abc"},
    ],
}

SAMPLE_IMAGE_FEED = {
    "images": [
        {
            "item_id": 12345,
            "headline": "ECB rate cut",
            "institution_code": "ECB",
            "generated_at": None,
            "formats": [
                {"format": "hero", "width": 1280, "height": 720, "url": "https://cms.state-of.biz/assets/abc"},
            ],
        }
    ],
    "total": 1,
}

SAMPLE_PURCHASE = {
    "credits_granted": 1000,
    "new_balance": 1000,
    "amount_lamports": 1000000,
    "credits_per_sol": 1000000,
}


# Route table for mock transport
ROUTES: dict[str, dict] = {
    "/api/items": {
        "items": [SAMPLE_ITEM],
        "total": 1,
        "page": 1,
        "per_page": 20,
    },
    "/api/semantic-search": SAMPLE_SEARCH_RESPONSE,
    "/api/rag-context": SAMPLE_RAG_RESPONSE,
    "/api/credits/balance": SAMPLE_BALANCE,
    "/api/premium/institutions": SAMPLE_INSTITUTIONS,
    "/api/premium/feed-status": SAMPLE_FEED_STATUS,
    "/api/premium/rates": SAMPLE_RATES,
    "/api/premium/sentiment": SAMPLE_SENTIMENT,
    "/api/premium/semantic-search": SAMPLE_SEARCH_RESPONSE,
    "/api/premium/rag-context": SAMPLE_RAG_RESPONSE,
    "/api/premium/briefing": SAMPLE_BRIEFING,
    "/api/premium/image-feed": SAMPLE_IMAGE_FEED,
    "/api/premium/cross-institution": SAMPLE_CROSS_INSTITUTION,
    "/api/premium/weekly-digest": SAMPLE_WEEKLY_DIGEST,
}


def _mock_handler(request: httpx.Request) -> httpx.Response:
    """Route requests to sample data."""
    path = request.url.path

    # Special cases
    if path.startswith("/api/item/") and not path.startswith("/api/items"):
        slug = path.split("/api/item/")[1]
        if slug == "not-found":
            return httpx.Response(404, json={"detail": "Item not found"})
        return httpx.Response(200, json=SAMPLE_ITEM)

    if path.startswith("/api/premium/image/") and "/api/premium/image-feed" not in path:
        parts = path.split("/")
        # /api/premium/image/{id}/{format} = 6 parts → redirect
        if len(parts) == 6:
            return httpx.Response(
                302, headers={"location": "https://cms.state-of.biz/assets/abc123"}
            )
        # /api/premium/image/{id} = 5 parts → metadata
        return httpx.Response(200, json=SAMPLE_IMAGE_METADATA)

    if path == "/api/credits/purchase" and request.method == "POST":
        return httpx.Response(200, json=SAMPLE_PURCHASE)

    if path in ROUTES:
        return httpx.Response(200, json=ROUTES[path])

    return httpx.Response(404, json={"detail": "Not found"})


def _mock_402_handler(request: httpx.Request) -> httpx.Response:
    """Always return 402."""
    import base64

    payment_req = {
        "scheme": "exact",
        "network": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
        "maxAmountRequired": "1000",
        "resource": str(request.url),
        "payTo": "TestPayTo",
        "asset": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    }
    return httpx.Response(
        402,
        json={"detail": "Payment Required"},
        headers={
            "X-Credits-Cost": "100",
            "X-Credits-Per-Sol": "1000000",
            "X-Wallet": "TestWallet",
            "X-Network": "devnet",
            "payment-required": base64.b64encode(json.dumps(payment_req).encode()).decode(),
        },
    )


def _mock_429_handler(request: httpx.Request) -> httpx.Response:
    """Always return 429."""
    return httpx.Response(
        429,
        json={"detail": "Rate limit exceeded"},
        headers={"Retry-After": "60"},
    )


@pytest.fixture
def mock_transport():
    """httpx MockTransport with SOB API routes."""
    return httpx.MockTransport(_mock_handler)


@pytest.fixture
def mock_402_transport():
    """httpx MockTransport that always returns 402."""
    return httpx.MockTransport(_mock_402_handler)


@pytest.fixture
def mock_429_transport():
    """httpx MockTransport that always returns 429."""
    return httpx.MockTransport(_mock_429_handler)


@pytest.fixture
def client(mock_transport):
    """SOBClient with mock transport."""
    from sob.client import SOBClient

    c = SOBClient(base_url="https://test.local", wallet="TestWallet123456789012345678901234")
    c._client = httpx.Client(transport=mock_transport, base_url="https://test.local")
    return c


@pytest.fixture
def async_client(mock_transport):
    """AsyncSOBClient with mock transport."""
    from sob.client import AsyncSOBClient

    c = AsyncSOBClient(base_url="https://test.local", wallet="TestWallet123456789012345678901234")
    c._client = httpx.AsyncClient(transport=mock_transport, base_url="https://test.local")
    return c
