"""Sync and async HTTP clients for the SOB API."""

from __future__ import annotations

from typing import Any

import httpx

from sob._constants import (
    BASE_URL,
    HEADER_API_KEY,
    HEADER_CREDITS_WALLET,
)
from sob.exceptions import (
    AuthenticationError,
    BadRequest,
    NotFound,
    PaymentRequired,
    RateLimited,
    ServerError,
    SOBError,
)
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


def _build_headers(
    api_key: str | None = None,
    wallet: str | None = None,
) -> dict[str, str]:
    headers: dict[str, str] = {}
    if api_key:
        headers[HEADER_API_KEY] = api_key
    if wallet:
        headers[HEADER_CREDITS_WALLET] = wallet
    return headers


def _handle_error(response: httpx.Response) -> None:
    """Raise typed exception for non-2xx responses."""
    if response.is_success:
        return
    status = response.status_code
    if status == 402:
        raise PaymentRequired.from_response(response)
    if status == 429:
        raise RateLimited.from_response(response)
    if status == 404:
        raise NotFound.from_response(response)
    if status == 401:
        raise AuthenticationError()
    if status == 400:
        raise BadRequest.from_response(response)
    if status >= 500:
        raise ServerError.from_response(response)
    raise SOBError(f"HTTP {status}", status_code=status)


def _clean_params(params: dict[str, Any]) -> dict[str, Any]:
    """Remove None values from query params."""
    return {k: v for k, v in params.items() if v is not None}


class SOBClient:
    """Synchronous client for the SOB API.

    Args:
        base_url: API base URL.
        api_key: Optional API key for higher rate limits (X-API-Key header).
        wallet: Optional Solana wallet address for premium endpoints (X-Credits-Wallet header).
        timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
        api_key: str | None = None,
        wallet: str | None = None,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.wallet = wallet
        self._client = httpx.Client(
            base_url=self.base_url,
            headers=_build_headers(api_key, wallet),
            timeout=timeout,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _get(self, path: str, params: dict | None = None) -> dict:
        params = _clean_params(params or {})
        response = self._client.get(path, params=params)
        _handle_error(response)
        return response.json()

    def _post(self, path: str, json_data: dict | None = None) -> dict:
        response = self._client.post(path, json=json_data)
        _handle_error(response)
        return response.json()

    # =====================================================================
    # Free Endpoints
    # =====================================================================

    def list_items(
        self,
        page: int = 1,
        per_page: int = 20,
        institution: str | None = None,
        category: str | None = None,
    ) -> ItemListResponse:
        """List enriched items with pagination and filtering."""
        data = self._get("/api/items", {
            "page": page,
            "per_page": per_page,
            "institution": institution,
            "category": category,
        })
        return ItemListResponse.model_validate(data)

    def get_item(self, slug: str) -> ItemResponse:
        """Get a single item by slug."""
        data = self._get(f"/api/item/{slug}")
        return ItemResponse.model_validate(data)

    def search(
        self,
        query: str,
        locale: str | None = None,
        institution: str | None = None,
        limit: int = 10,
    ) -> SemanticSearchResponse:
        """Free semantic search (up to 50 results)."""
        data = self._get("/api/semantic-search", {
            "q": query,
            "locale": locale,
            "institution": institution,
            "limit": limit,
        })
        return SemanticSearchResponse.model_validate(data)

    def get_rag_context(
        self,
        query: str,
        locale: str | None = None,
        max_tokens: int = 2000,
    ) -> RAGContextResponse:
        """Free RAG context retrieval (up to 8000 tokens)."""
        data = self._get("/api/rag-context", {
            "q": query,
            "locale": locale,
            "max_tokens": max_tokens,
        })
        return RAGContextResponse.model_validate(data)

    # =====================================================================
    # Premium Tier 1 (1 Credit) — Metadata
    # =====================================================================

    def get_institutions(self) -> InstitutionsResponse:
        """List all institutions with feed health. Tier 1: 1 credit."""
        data = self._get("/api/premium/institutions")
        return InstitutionsResponse.model_validate(data)

    def get_feed_status(self) -> FeedStatusResponse:
        """Pipeline throughput and health metrics. Tier 1: 1 credit."""
        data = self._get("/api/premium/feed-status")
        return FeedStatusResponse.model_validate(data)

    # =====================================================================
    # Premium Tier 2 (10 Credits) — Structured Data
    # =====================================================================

    def get_rates(self, institution: str | None = None) -> RatesResponse:
        """Key rates extracted from central bank items. Tier 2: 10 credits."""
        data = self._get("/api/premium/rates", {"institution": institution})
        return RatesResponse.model_validate(data)

    def get_sentiment(
        self,
        institution: str | None = None,
        days: int = 7,
    ) -> SentimentResponse:
        """Policy stance indicators from recent items. Tier 2: 10 credits."""
        data = self._get("/api/premium/sentiment", {
            "institution": institution,
            "days": days,
        })
        return SentimentResponse.model_validate(data)

    def get_image(self, item_id: int) -> ImageMetadataResponse:
        """Image metadata and format URLs. Tier 2: 10 credits."""
        data = self._get(f"/api/premium/image/{item_id}")
        return ImageMetadataResponse.model_validate(data)

    def get_image_url(self, item_id: int, format: str = "hero") -> str:
        """Get redirect URL for a specific image format. Tier 2: 10 credits.

        Note: This follows the redirect and returns the final URL.
        """
        response = self._client.get(
            f"/api/premium/image/{item_id}/{format}",
            follow_redirects=False,
        )
        if response.status_code == 302:
            return response.headers["location"]
        _handle_error(response)
        return response.headers.get("location", "")

    # =====================================================================
    # Premium Tier 3 (100 Credits) — Semantic Objects
    # =====================================================================

    def premium_search(
        self,
        query: str,
        locale: str | None = None,
        institution: str | None = None,
        limit: int = 20,
    ) -> SemanticSearchResponse:
        """Premium semantic search with higher limits. Tier 3: 100 credits."""
        data = self._get("/api/premium/semantic-search", {
            "q": query,
            "locale": locale,
            "institution": institution,
            "limit": limit,
        })
        return SemanticSearchResponse.model_validate(data)

    def premium_rag_context(
        self,
        query: str,
        locale: str | None = None,
        max_tokens: int = 4000,
    ) -> RAGContextResponse:
        """Premium RAG context with larger token budget. Tier 3: 100 credits."""
        data = self._get("/api/premium/rag-context", {
            "q": query,
            "locale": locale,
            "max_tokens": max_tokens,
        })
        return RAGContextResponse.model_validate(data)

    def get_briefing(
        self,
        item_id: int,
        locale: str = "en",
    ) -> BriefingResponse:
        """Full item briefing with all enrichment data. Tier 3: 100 credits."""
        data = self._get("/api/premium/briefing", {
            "item_id": item_id,
            "locale": locale,
        })
        return BriefingResponse.model_validate(data)

    def get_image_feed(
        self,
        limit: int = 20,
        institution: str | None = None,
    ) -> ImageFeedResponse:
        """Latest images as JSON feed. Tier 3: 100 credits."""
        data = self._get("/api/premium/image-feed", {
            "limit": limit,
            "institution": institution,
        })
        return ImageFeedResponse.model_validate(data)

    # =====================================================================
    # Premium Tier 4 (1000 Credits) — Composite Reports
    # =====================================================================

    def get_cross_institution(
        self,
        institutions: list[str],
        days: int = 7,
        locale: str = "en",
    ) -> CrossInstitutionResponse:
        """Multi-institution comparison. Tier 4: 1000 credits."""
        data = self._get("/api/premium/cross-institution", {
            "institutions": ",".join(institutions),
            "days": days,
            "locale": locale,
        })
        return CrossInstitutionResponse.model_validate(data)

    def get_weekly_digest(
        self,
        locale: str = "en",
        institution: str | None = None,
    ) -> WeeklyDigestResponse:
        """Weekly digest summary. Tier 4: 1000 credits."""
        data = self._get("/api/premium/weekly-digest", {
            "locale": locale,
            "institution": institution,
        })
        return WeeklyDigestResponse.model_validate(data)

    # =====================================================================
    # Credits
    # =====================================================================

    def get_balance(self, wallet: str | None = None) -> CreditBalanceResponse:
        """Check credit balance for a wallet.

        Uses the client's wallet if none specified.
        """
        w = wallet or self.wallet
        if not w:
            raise ValueError("No wallet specified")
        data = self._get("/api/credits/balance", {"wallet": w})
        return CreditBalanceResponse.model_validate(data)

    def purchase_credits(
        self, tx_signature: str, wallet: str | None = None,
    ) -> CreditPurchaseResponse:
        """Purchase credits with a Solana TX signature.

        Args:
            tx_signature: Base58-encoded Solana transaction signature.
            wallet: Wallet address (uses client wallet if not specified).
        """
        w = wallet or self.wallet
        if not w:
            raise ValueError("No wallet specified")
        data = self._post("/api/credits/purchase", {
            "tx_signature": tx_signature,
            "wallet": w,
        })
        return CreditPurchaseResponse.model_validate(data)


class AsyncSOBClient:
    """Asynchronous client for the SOB API.

    Same API as SOBClient but all methods are async.

    Args:
        base_url: API base URL.
        api_key: Optional API key for higher rate limits (X-API-Key header).
        wallet: Optional Solana wallet address for premium endpoints (X-Credits-Wallet header).
        timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
        api_key: str | None = None,
        wallet: str | None = None,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.wallet = wallet
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=_build_headers(api_key, wallet),
            timeout=timeout,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def _get(self, path: str, params: dict | None = None) -> dict:
        params = _clean_params(params or {})
        response = await self._client.get(path, params=params)
        _handle_error(response)
        return response.json()

    async def _post(self, path: str, json_data: dict | None = None) -> dict:
        response = await self._client.post(path, json=json_data)
        _handle_error(response)
        return response.json()

    # =====================================================================
    # Free Endpoints
    # =====================================================================

    async def list_items(
        self,
        page: int = 1,
        per_page: int = 20,
        institution: str | None = None,
        category: str | None = None,
    ) -> ItemListResponse:
        data = await self._get("/api/items", {
            "page": page,
            "per_page": per_page,
            "institution": institution,
            "category": category,
        })
        return ItemListResponse.model_validate(data)

    async def get_item(self, slug: str) -> ItemResponse:
        data = await self._get(f"/api/item/{slug}")
        return ItemResponse.model_validate(data)

    async def search(
        self,
        query: str,
        locale: str | None = None,
        institution: str | None = None,
        limit: int = 10,
    ) -> SemanticSearchResponse:
        data = await self._get("/api/semantic-search", {
            "q": query,
            "locale": locale,
            "institution": institution,
            "limit": limit,
        })
        return SemanticSearchResponse.model_validate(data)

    async def get_rag_context(
        self,
        query: str,
        locale: str | None = None,
        max_tokens: int = 2000,
    ) -> RAGContextResponse:
        data = await self._get("/api/rag-context", {
            "q": query,
            "locale": locale,
            "max_tokens": max_tokens,
        })
        return RAGContextResponse.model_validate(data)

    # =====================================================================
    # Premium Tier 1
    # =====================================================================

    async def get_institutions(self) -> InstitutionsResponse:
        data = await self._get("/api/premium/institutions")
        return InstitutionsResponse.model_validate(data)

    async def get_feed_status(self) -> FeedStatusResponse:
        data = await self._get("/api/premium/feed-status")
        return FeedStatusResponse.model_validate(data)

    # =====================================================================
    # Premium Tier 2
    # =====================================================================

    async def get_rates(self, institution: str | None = None) -> RatesResponse:
        data = await self._get("/api/premium/rates", {"institution": institution})
        return RatesResponse.model_validate(data)

    async def get_sentiment(
        self,
        institution: str | None = None,
        days: int = 7,
    ) -> SentimentResponse:
        data = await self._get("/api/premium/sentiment", {
            "institution": institution,
            "days": days,
        })
        return SentimentResponse.model_validate(data)

    async def get_image(self, item_id: int) -> ImageMetadataResponse:
        data = await self._get(f"/api/premium/image/{item_id}")
        return ImageMetadataResponse.model_validate(data)

    async def get_image_url(self, item_id: int, format: str = "hero") -> str:
        response = await self._client.get(
            f"/api/premium/image/{item_id}/{format}",
            follow_redirects=False,
        )
        if response.status_code == 302:
            return response.headers["location"]
        _handle_error(response)
        return response.headers.get("location", "")

    # =====================================================================
    # Premium Tier 3
    # =====================================================================

    async def premium_search(
        self,
        query: str,
        locale: str | None = None,
        institution: str | None = None,
        limit: int = 20,
    ) -> SemanticSearchResponse:
        data = await self._get("/api/premium/semantic-search", {
            "q": query,
            "locale": locale,
            "institution": institution,
            "limit": limit,
        })
        return SemanticSearchResponse.model_validate(data)

    async def premium_rag_context(
        self,
        query: str,
        locale: str | None = None,
        max_tokens: int = 4000,
    ) -> RAGContextResponse:
        data = await self._get("/api/premium/rag-context", {
            "q": query,
            "locale": locale,
            "max_tokens": max_tokens,
        })
        return RAGContextResponse.model_validate(data)

    async def get_briefing(
        self,
        item_id: int,
        locale: str = "en",
    ) -> BriefingResponse:
        data = await self._get("/api/premium/briefing", {
            "item_id": item_id,
            "locale": locale,
        })
        return BriefingResponse.model_validate(data)

    async def get_image_feed(
        self,
        limit: int = 20,
        institution: str | None = None,
    ) -> ImageFeedResponse:
        data = await self._get("/api/premium/image-feed", {
            "limit": limit,
            "institution": institution,
        })
        return ImageFeedResponse.model_validate(data)

    # =====================================================================
    # Premium Tier 4
    # =====================================================================

    async def get_cross_institution(
        self,
        institutions: list[str],
        days: int = 7,
        locale: str = "en",
    ) -> CrossInstitutionResponse:
        data = await self._get("/api/premium/cross-institution", {
            "institutions": ",".join(institutions),
            "days": days,
            "locale": locale,
        })
        return CrossInstitutionResponse.model_validate(data)

    async def get_weekly_digest(
        self,
        locale: str = "en",
        institution: str | None = None,
    ) -> WeeklyDigestResponse:
        data = await self._get("/api/premium/weekly-digest", {
            "locale": locale,
            "institution": institution,
        })
        return WeeklyDigestResponse.model_validate(data)

    # =====================================================================
    # Credits
    # =====================================================================

    async def get_balance(self, wallet: str | None = None) -> CreditBalanceResponse:
        w = wallet or self.wallet
        if not w:
            raise ValueError("No wallet specified")
        data = await self._get("/api/credits/balance", {"wallet": w})
        return CreditBalanceResponse.model_validate(data)

    async def purchase_credits(
        self, tx_signature: str, wallet: str | None = None,
    ) -> CreditPurchaseResponse:
        w = wallet or self.wallet
        if not w:
            raise ValueError("No wallet specified")
        data = await self._post("/api/credits/purchase", {
            "tx_signature": tx_signature,
            "wallet": w,
        })
        return CreditPurchaseResponse.model_validate(data)
