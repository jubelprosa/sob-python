"""Tests for LlamaIndex SOBReader integration."""

import httpx
import pytest

from tests.conftest import _mock_handler


@pytest.fixture
def reader():
    from sob.integrations.llamaindex import SOBReader

    r = SOBReader(base_url="https://test.local")
    r._client._client = httpx.Client(
        transport=httpx.MockTransport(_mock_handler), base_url="https://test.local"
    )
    return r


class TestSOBReader:
    def test_search_mode(self, reader):
        docs = reader.load_data(query="ECB interest rate")
        assert len(docs) == 1
        assert "ECB cuts rate" in docs[0].text
        assert docs[0].metadata["source"] == "sob"

    def test_rag_mode(self, reader):
        reader.mode = "rag"
        docs = reader.load_data(query="ECB monetary policy")
        assert len(docs) == 1
        assert "Full text" in docs[0].text

    def test_items_mode(self, reader):
        reader.mode = "items"
        docs = reader.load_data()
        assert len(docs) == 1
        assert docs[0].metadata["institution_code"] == "ECB"

    def test_search_requires_query(self, reader):
        with pytest.raises(ValueError, match="Query required"):
            reader.load_data()

    def test_rag_requires_query(self, reader):
        reader.mode = "rag"
        with pytest.raises(ValueError, match="Query required"):
            reader.load_data()

    def test_items_no_query_needed(self, reader):
        reader.mode = "items"
        docs = reader.load_data()
        assert len(docs) >= 1

    def test_premium_search(self, reader):
        reader.premium = True
        docs = reader.load_data(query="ECB rate")
        assert len(docs) == 1

    def test_premium_rag(self, reader):
        reader.mode = "rag"
        reader.premium = True
        docs = reader.load_data(query="ECB policy")
        assert len(docs) == 1

    def test_metadata_fields(self, reader):
        docs = reader.load_data(query="ECB")
        meta = docs[0].metadata
        assert "id" in meta
        assert "slug" in meta
        assert "similarity" in meta

    def test_institution_filter(self, reader):
        reader.mode = "items"
        docs = reader.load_data(institution="ECB", limit=5)
        assert len(docs) >= 1
