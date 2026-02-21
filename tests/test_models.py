"""Tests for Pydantic response models."""

from sob.models import (
    BriefingResponse,
    CreditBalanceResponse,
    CreditPurchaseResponse,
    CrossInstitutionResponse,
    FeedStatusResponse,
    ImageFeedResponse,
    ImageMetadataResponse,
    InstitutionsResponse,
    ItemListResponse,
    ItemResponse,
    RAGContextResponse,
    RatesResponse,
    SemanticSearchResponse,
    SentimentResponse,
    WeeklyDigestResponse,
)
from tests.conftest import (
    SAMPLE_BALANCE,
    SAMPLE_BRIEFING,
    SAMPLE_CROSS_INSTITUTION,
    SAMPLE_FEED_STATUS,
    SAMPLE_IMAGE_FEED,
    SAMPLE_IMAGE_METADATA,
    SAMPLE_INSTITUTIONS,
    SAMPLE_ITEM,
    SAMPLE_PURCHASE,
    SAMPLE_RAG_RESPONSE,
    SAMPLE_RATES,
    SAMPLE_SEARCH_RESPONSE,
    SAMPLE_SENTIMENT,
    SAMPLE_WEEKLY_DIGEST,
)


def test_item_response():
    item = ItemResponse.model_validate(SAMPLE_ITEM)
    assert item.id == 12345
    assert item.slug == "ecb-rate-cut-january-2026"
    assert item.institution_code == "ECB"
    assert item.content is not None
    assert item.content.headline == "ECB cuts interest rate to 2.75 percent"


def test_item_list_response():
    data = {"items": [SAMPLE_ITEM], "total": 1, "page": 1, "per_page": 20}
    resp = ItemListResponse.model_validate(data)
    assert resp.total == 1
    assert len(resp.items) == 1
    assert resp.items[0].id == 12345


def test_semantic_search_response():
    resp = SemanticSearchResponse.model_validate(SAMPLE_SEARCH_RESPONSE)
    assert resp.query == "ECB interest rate"
    assert len(resp.items) == 1
    assert resp.items[0].similarity == 0.9234


def test_rag_context_response():
    resp = RAGContextResponse.model_validate(SAMPLE_RAG_RESPONSE)
    assert resp.total_tokens_estimate == 500
    assert resp.items[0].body_text == "Full text of the ECB decision..."


def test_credit_balance_response():
    resp = CreditBalanceResponse.model_validate(SAMPLE_BALANCE)
    assert resp.balance == 850
    assert resp.total_purchased == 1000


def test_credit_purchase_response():
    resp = CreditPurchaseResponse.model_validate(SAMPLE_PURCHASE)
    assert resp.credits_granted == 1000
    assert resp.credits_per_sol == 1000000


def test_institutions_response():
    resp = InstitutionsResponse.model_validate(SAMPLE_INSTITUTIONS)
    assert resp.total == 1
    assert resp.institutions[0].code == "ECB"


def test_feed_status_response():
    resp = FeedStatusResponse.model_validate(SAMPLE_FEED_STATUS)
    assert len(resp.daily_stats) == 1
    assert resp.pipeline_status["published"] == 12500


def test_rates_response():
    resp = RatesResponse.model_validate(SAMPLE_RATES)
    assert resp.rates[0].label == "Deposit Rate"
    assert resp.rates[0].value == "2.75%"


def test_sentiment_response():
    resp = SentimentResponse.model_validate(SAMPLE_SENTIMENT)
    assert resp.period_days == 7
    assert resp.sentiments[0].institution == "FED"


def test_briefing_response():
    resp = BriefingResponse.model_validate(SAMPLE_BRIEFING)
    assert resp.id == 12345
    assert resp.content["headline"] == "ECB cuts rate"


def test_cross_institution_response():
    resp = CrossInstitutionResponse.model_validate(SAMPLE_CROSS_INSTITUTION)
    assert resp.period_days == 7
    assert resp.total_items == 1


def test_weekly_digest_response():
    resp = WeeklyDigestResponse.model_validate(SAMPLE_WEEKLY_DIGEST)
    assert resp.period == "7 days"
    assert "Press" in resp.by_category


def test_image_metadata_response():
    resp = ImageMetadataResponse.model_validate(SAMPLE_IMAGE_METADATA)
    assert resp.item_id == 12345
    assert len(resp.formats) == 1


def test_image_feed_response():
    resp = ImageFeedResponse.model_validate(SAMPLE_IMAGE_FEED)
    assert resp.total == 1
    assert resp.images[0].item_id == 12345


def test_item_with_minimal_data():
    """Ensure optional fields default to None."""
    minimal = {
        "id": 1,
        "slug": "test",
        "url": "https://example.com",
        "title": "Test",
        "institution_code": "ECB",
        "institution_name": "ECB",
        "status": "published",
    }
    item = ItemResponse.model_validate(minimal)
    assert item.content is None
    assert item.classification is None
    assert item.published_at is None
