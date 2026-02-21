"""LlamaIndex integration for the SOB API.

Provides SOBReader — a LlamaIndex BaseReader that loads central bank
documents from the SOB API.

Install: pip install "sob-python[llamaindex]"
"""

from __future__ import annotations

from typing import Literal

from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document

from sob.client import SOBClient


class SOBReader(BaseReader):
    """LlamaIndex reader for SOB central bank intelligence.

    Args:
        mode: "search" for semantic search, "rag" for full RAG context,
              "items" for item listing (no query needed).
        premium: Use premium endpoints (requires wallet with credits).
        base_url: SOB API base URL.
        api_key: Optional API key for higher rate limits.
        wallet: Solana wallet address for premium access.
    """

    def __init__(
        self,
        mode: Literal["search", "rag", "items"] = "search",
        premium: bool = False,
        base_url: str = "https://state-of.biz",
        api_key: str | None = None,
        wallet: str | None = None,
    ):
        super().__init__()
        self.mode = mode
        self.premium = premium
        self._client = SOBClient(
            base_url=base_url,
            api_key=api_key,
            wallet=wallet,
        )

    def load_data(
        self,
        query: str | None = None,
        institution: str | None = None,
        locale: str | None = None,
        limit: int = 10,
        max_tokens: int = 2000,
    ) -> list[Document]:
        """Load documents from the SOB API.

        Args:
            query: Search query (required for search/rag modes).
            institution: Filter by institution code.
            locale: Filter by locale (en, de).
            limit: Max results for search/items modes.
            max_tokens: Token budget for rag mode.
        """
        if self.mode == "items":
            return self._load_items(institution=institution, limit=limit)
        elif self.mode == "rag":
            if not query:
                raise ValueError("Query required for rag mode")
            return self._load_rag(query, locale=locale, max_tokens=max_tokens)
        else:
            if not query:
                raise ValueError("Query required for search mode")
            return self._load_search(
                query, locale=locale, institution=institution, limit=limit
            )

    def _load_items(
        self,
        institution: str | None = None,
        limit: int = 10,
    ) -> list[Document]:
        resp = self._client.list_items(per_page=limit, institution=institution)
        return [
            Document(
                text=f"{item.content.headline if item.content else item.title}\n\n"
                     f"{item.content.lead if item.content else ''}",
                metadata={
                    "id": item.id,
                    "slug": item.slug,
                    "url": item.url,
                    "title": item.title,
                    "institution_code": item.institution_code,
                    "institution_name": item.institution_name,
                    "status": item.status,
                    "published_at": str(item.published_at) if item.published_at else None,
                    "source": "sob",
                },
            )
            for item in resp.items
        ]

    def _load_search(
        self,
        query: str,
        locale: str | None = None,
        institution: str | None = None,
        limit: int = 10,
    ) -> list[Document]:
        if self.premium:
            resp = self._client.premium_search(
                query, locale=locale, institution=institution, limit=limit
            )
        else:
            resp = self._client.search(
                query, locale=locale, institution=institution, limit=limit
            )
        return [
            Document(
                text=f"{item.headline}\n\n{item.lead}",
                metadata={
                    "id": item.id,
                    "slug": item.slug,
                    "url": item.url,
                    "title": item.title,
                    "institution_code": item.institution_code,
                    "institution_name": item.institution_name,
                    "similarity": item.similarity,
                    "published_at": str(item.published_at) if item.published_at else None,
                    "source": "sob",
                },
            )
            for item in resp.items
        ]

    def _load_rag(
        self,
        query: str,
        locale: str | None = None,
        max_tokens: int = 2000,
    ) -> list[Document]:
        if self.premium:
            resp = self._client.premium_rag_context(
                query, locale=locale, max_tokens=max_tokens
            )
        else:
            resp = self._client.get_rag_context(
                query, locale=locale, max_tokens=max_tokens
            )
        return [
            Document(
                text=f"{item.headline}\n\n{item.body_text}",
                metadata={
                    "id": item.id,
                    "headline": item.headline,
                    "lead": item.lead,
                    "institution": item.institution,
                    "source_url": item.source_url,
                    "published_at": item.published_at,
                    "similarity": item.similarity,
                    "source": "sob",
                },
            )
            for item in resp.items
        ]
