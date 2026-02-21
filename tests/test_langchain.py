"""Tests for LangChain SOBRetriever integration."""

import httpx
import pytest

from tests.conftest import _mock_handler


@pytest.fixture
def retriever():
    from sob.integrations.langchain import SOBRetriever

    r = SOBRetriever(k=5, base_url="https://test.local")
    # Inject mock transport into the internal client
    from sob.client import SOBClient

    c = SOBClient(base_url="https://test.local")
    c._client = httpx.Client(transport=httpx.MockTransport(_mock_handler), base_url="https://test.local")
    r._client = c
    return r


class TestSOBRetriever:
    def test_search_mode(self, retriever):
        docs = retriever.invoke("ECB interest rate")
        assert len(docs) == 1
        assert "ECB cuts rate" in docs[0].page_content
        assert docs[0].metadata["source"] == "sob"
        assert docs[0].metadata["institution_code"] == "ECB"

    def test_rag_mode(self, retriever):
        retriever.mode = "rag"
        docs = retriever.invoke("ECB monetary policy")
        assert len(docs) == 1
        assert "Full text" in docs[0].page_content
        assert docs[0].metadata["source"] == "sob"
        assert docs[0].metadata["institution"] == "European Central Bank"

    def test_premium_search_mode(self, retriever):
        retriever.premium = True
        docs = retriever.invoke("ECB rate decision")
        assert len(docs) == 1

    def test_premium_rag_mode(self, retriever):
        retriever.mode = "rag"
        retriever.premium = True
        docs = retriever.invoke("ECB policy")
        assert len(docs) == 1

    def test_metadata_fields(self, retriever):
        docs = retriever.invoke("ECB")
        meta = docs[0].metadata
        assert "id" in meta
        assert "slug" in meta
        assert "similarity" in meta

    def test_creates_client_lazily(self):
        from sob.integrations.langchain import SOBRetriever

        r = SOBRetriever(base_url="https://test.local")
        assert r._client is None
        # _get_client should create one
        client = r._get_client()
        assert client is not None
        client.close()
