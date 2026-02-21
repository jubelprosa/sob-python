"""Tests for the async AsyncSOBClient."""

import httpx
import pytest

from sob.client import AsyncSOBClient
from sob.exceptions import NotFound, PaymentRequired, RateLimited


@pytest.mark.asyncio
class TestAsyncFreeEndpoints:
    async def test_list_items(self, async_client):
        resp = await async_client.list_items()
        assert resp.total == 1

    async def test_get_item(self, async_client):
        item = await async_client.get_item("ecb-rate-cut-january-2026")
        assert item.id == 12345

    async def test_get_item_not_found(self, async_client):
        with pytest.raises(NotFound):
            await async_client.get_item("not-found")

    async def test_search(self, async_client):
        resp = await async_client.search("ECB interest rate")
        assert resp.total == 1

    async def test_get_rag_context(self, async_client):
        resp = await async_client.get_rag_context("ECB monetary policy")
        assert resp.total_tokens_estimate == 500


@pytest.mark.asyncio
class TestAsyncPremiumEndpoints:
    async def test_get_institutions(self, async_client):
        resp = await async_client.get_institutions()
        assert resp.total == 1

    async def test_get_feed_status(self, async_client):
        resp = await async_client.get_feed_status()
        assert len(resp.daily_stats) == 1

    async def test_get_rates(self, async_client):
        resp = await async_client.get_rates()
        assert resp.rates[0].label == "Deposit Rate"

    async def test_get_sentiment(self, async_client):
        resp = await async_client.get_sentiment()
        assert resp.period_days == 7

    async def test_get_image(self, async_client):
        resp = await async_client.get_image(12345)
        assert resp.item_id == 12345

    async def test_get_image_url(self, async_client):
        url = await async_client.get_image_url(12345, format="hero")
        assert "cms.state-of.biz" in url

    async def test_premium_search(self, async_client):
        resp = await async_client.premium_search("ECB rate")
        assert resp.total == 1

    async def test_premium_rag_context(self, async_client):
        resp = await async_client.premium_rag_context("ECB policy")
        assert resp.total_tokens_estimate == 500

    async def test_get_briefing(self, async_client):
        resp = await async_client.get_briefing(12345)
        assert resp.id == 12345

    async def test_get_image_feed(self, async_client):
        resp = await async_client.get_image_feed()
        assert resp.total == 1

    async def test_get_cross_institution(self, async_client):
        resp = await async_client.get_cross_institution(["ECB", "FED"])
        assert resp.period_days == 7

    async def test_get_weekly_digest(self, async_client):
        resp = await async_client.get_weekly_digest()
        assert resp.period == "7 days"


@pytest.mark.asyncio
class TestAsyncCredits:
    async def test_get_balance(self, async_client):
        resp = await async_client.get_balance()
        assert resp.balance == 850

    async def test_purchase_credits(self, async_client):
        resp = await async_client.purchase_credits("TxSig123")
        assert resp.credits_granted == 1000

    async def test_get_balance_no_wallet(self):
        c = AsyncSOBClient()
        with pytest.raises(ValueError, match="No wallet"):
            await c.get_balance()
        await c.close()


@pytest.mark.asyncio
class TestAsyncErrorHandling:
    async def test_402_payment_required(self, mock_402_transport):
        c = AsyncSOBClient(base_url="https://test.local")
        c._client = httpx.AsyncClient(transport=mock_402_transport, base_url="https://test.local")
        with pytest.raises(PaymentRequired):
            await c.get_institutions()
        await c.close()

    async def test_429_rate_limited(self, mock_429_transport):
        c = AsyncSOBClient(base_url="https://test.local")
        c._client = httpx.AsyncClient(transport=mock_429_transport, base_url="https://test.local")
        with pytest.raises(RateLimited):
            await c.list_items()
        await c.close()


@pytest.mark.asyncio
class TestAsyncLifecycle:
    async def test_context_manager(self, mock_transport):
        async with AsyncSOBClient(base_url="https://test.local") as c:
            c._client = httpx.AsyncClient(transport=mock_transport, base_url="https://test.local")
            resp = await c.list_items()
            assert resp.total == 1
