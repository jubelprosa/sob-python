"""Pydantic v2 response models for the SOB API."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel

# =============================================================================
# Item Models
# =============================================================================


class Content(BaseModel):
    headline: str = ""
    lead: str = ""
    body: dict | None = None
    quote: dict | None = None
    key_facts: list | None = None


class Classification(BaseModel):
    category: str | None = None
    communication_type: str | None = None
    content_density: str | None = None
    policy_areas: list[str] | None = None


class NextEvent(BaseModel):
    date: str
    type: str
    description: str | None = None


class DocumentMeta(BaseModel):
    pages: int | None = None
    word_count: int | None = None
    language: str | None = None


class ProcessingMeta(BaseModel):
    model: str | None = None
    prompt_version: str | None = None
    duration_ms: int | None = None
    tokens_in: int | None = None
    tokens_out: int | None = None


class ItemResponse(BaseModel):
    id: int
    slug: str
    url: str
    title: str
    institution_code: str
    institution_name: str
    status: str
    published_at: datetime | None = None
    enriched_at: datetime | None = None
    content: Content | None = None
    classification: Classification | None = None
    source_url: str | None = None
    processed_at: datetime | None = None
    processing: ProcessingMeta | None = None
    document: DocumentMeta | None = None
    next_event: NextEvent | None = None


class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    per_page: int


# =============================================================================
# Semantic Search Models
# =============================================================================


class SemanticSearchItem(BaseModel):
    id: int
    slug: str
    url: str
    title: str
    headline: str
    lead: str
    institution_code: str
    institution_name: str
    similarity: float
    published_at: datetime | None = None


class SemanticSearchResponse(BaseModel):
    query: str
    items: list[SemanticSearchItem]
    total: int


# =============================================================================
# RAG Context Models
# =============================================================================


class RAGContextItem(BaseModel):
    id: int
    headline: str
    lead: str
    body_text: str
    institution: str
    published_at: str | None = None
    source_url: str
    similarity: float


class RAGContextResponse(BaseModel):
    query: str
    items: list[RAGContextItem]
    total_tokens_estimate: int


# =============================================================================
# Credit Models
# =============================================================================


class CreditBalanceResponse(BaseModel):
    wallet: str
    balance: int
    total_purchased: int
    total_spent: int


class CreditPurchaseResponse(BaseModel):
    credits_granted: int
    new_balance: int
    amount_lamports: int
    credits_per_sol: int


# =============================================================================
# Premium Tier 1 Models
# =============================================================================


class InstitutionItem(BaseModel):
    code: str
    name: str
    active: bool
    total_items: int
    published_items: int
    failed_items: int
    latest_item_at: str | None = None


class InstitutionsResponse(BaseModel):
    institutions: list[InstitutionItem]
    total: int


class DailyStat(BaseModel):
    day: date
    items: int
    institutions: int


class FeedStatusResponse(BaseModel):
    daily_stats: list[DailyStat]
    pipeline_status: dict[str, int]


# =============================================================================
# Premium Tier 2 Models
# =============================================================================


class RateItem(BaseModel):
    institution: str
    institution_name: str
    label: str
    value: str
    change: str | None = None
    source_date: str | None = None


class RatesResponse(BaseModel):
    rates: list[RateItem]
    total: int


class SentimentItem(BaseModel):
    institution: str
    institution_name: str
    category: str
    communication_type: str
    policy_areas: list[str]
    headline: str
    published_at: str | None = None


class SentimentResponse(BaseModel):
    sentiments: list[SentimentItem]
    total: int
    period_days: int


class ImageFormat(BaseModel):
    format: str
    width: int
    height: int
    url: str


class ImageMetadataResponse(BaseModel):
    item_id: int
    headline: str
    institution_code: str
    image_prompt: str | None = None
    generated_at: str | None = None
    formats: list[ImageFormat]


# =============================================================================
# Premium Tier 3 Models
# =============================================================================


class BriefingResponse(BaseModel):
    id: int
    slug: str
    url: str
    title: str
    institution_code: str
    institution_name: str
    published_at: str | None = None
    content: dict
    classification: dict
    temporal: dict
    extraction: dict
    processing: dict


class ImageFeedItem(BaseModel):
    item_id: int
    headline: str
    institution_code: str
    generated_at: str | None = None
    formats: list[ImageFormat]


class ImageFeedResponse(BaseModel):
    images: list[ImageFeedItem]
    total: int


# =============================================================================
# Premium Tier 4 Models
# =============================================================================


class CrossInstitutionGroup(BaseModel):
    institution_code: str
    institution_name: str
    items: list[dict]


class CrossInstitutionResponse(BaseModel):
    institutions: list[CrossInstitutionGroup]
    period_days: int
    total_items: int


class WeeklyDigestResponse(BaseModel):
    period: str
    total_items: int
    by_category: dict[str, list[dict]]
    by_institution: dict[str, list[dict]]
