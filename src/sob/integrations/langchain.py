"""LangChain integration for the SOB API.

Provides SOBRetriever — a LangChain BaseRetriever that fetches central bank
documents via semantic search or RAG context.

Install: pip install "sob-python[langchain]"
"""

from __future__ import annotations

from typing import Literal

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import PrivateAttr

from sob.client import SOBClient


class SOBRetriever(BaseRetriever):
    """LangChain retriever for SOB central bank intelligence.

    Args:
        mode: "search" for semantic search results, "rag" for full RAG context.
        k: Number of results (search mode) or max tokens / 400 estimate (rag mode).
        locale: Filter by locale (en, de).
        institution: Filter by institution code (e.g. ECB, FED).
        premium: Use premium endpoints (requires wallet with credits).
        base_url: SOB API base URL.
        api_key: Optional API key for higher rate limits.
        wallet: Solana wallet address for premium access.
    """

    mode: Literal["search", "rag"] = "search"
    k: int = 5
    locale: str | None = None
    institution: str | None = None
    premium: bool = False
    base_url: str = "https://state-of.biz"
    api_key: str | None = None
    wallet: str | None = None

    _client: SOBClient | None = PrivateAttr(default=None)

    def _get_client(self) -> SOBClient:
        if self._client is None:
            self._client = SOBClient(
                base_url=self.base_url,
                api_key=self.api_key,
                wallet=self.wallet,
            )
        return self._client

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun | None = None,
    ) -> list[Document]:
        client = self._get_client()

        if self.mode == "rag":
            max_tokens = self.k * 400  # rough estimate
            if self.premium:
                resp = client.premium_rag_context(
                    query, locale=self.locale, max_tokens=max_tokens
                )
            else:
                resp = client.get_rag_context(
                    query, locale=self.locale, max_tokens=max_tokens
                )
            return [
                Document(
                    page_content=f"{item.headline}\n\n{item.body_text}",
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
        else:
            # search mode
            if self.premium:
                resp = client.premium_search(
                    query,
                    locale=self.locale,
                    institution=self.institution,
                    limit=self.k,
                )
            else:
                resp = client.search(
                    query,
                    locale=self.locale,
                    institution=self.institution,
                    limit=self.k,
                )
            return [
                Document(
                    page_content=f"{item.headline}\n\n{item.lead}",
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
