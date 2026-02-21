"""Tests for the synchronous SOBClient."""

import httpx
import pytest

from sob.client import SOBClient
from sob.exceptions import NotFound, PaymentRequired, RateLimited


class TestFreeEndpoints:
    def test_list_items(self, client):
        resp = client.list_items()
        assert resp.total == 1
        assert resp.items[0].slug == "ecb-rate-cut-january-2026"

    def test_list_items_with_filters(self, client):
        resp = client.list_items(page=1, per_page=10, institution="ECB", category="Press")
        assert resp.total == 1

    def test_get_item(self, client):
        item = client.get_item("ecb-rate-cut-january-2026")
        assert item.id == 12345
        assert item.institution_code == "ECB"

    def test_get_item_not_found(self, client):
        with pytest.raises(NotFound):
            client.get_item("not-found")

    def test_search(self, client):
        resp = client.search("ECB interest rate")
        assert resp.total == 1
        assert resp.items[0].similarity == 0.9234

    def test_search_with_filters(self, client):
        resp = client.search("ECB", locale="en", institution="ECB", limit=5)
        assert resp.total == 1

    def test_get_rag_context(self, client):
        resp = client.get_rag_context("ECB monetary policy")
        assert resp.total_tokens_estimate == 500
        assert len(resp.items) == 1


class TestPremiumEndpoints:
    def test_get_institutions(self, client):
        resp = client.get_institutions()
        assert resp.total == 1
        assert resp.institutions[0].code == "ECB"

    def test_get_feed_status(self, client):
        resp = client.get_feed_status()
        assert len(resp.daily_stats) == 1

    def test_get_rates(self, client):
        resp = client.get_rates()
        assert resp.rates[0].label == "Deposit Rate"

    def test_get_rates_filtered(self, client):
        resp = client.get_rates(institution="ECB")
        assert resp.total == 1

    def test_get_sentiment(self, client):
        resp = client.get_sentiment(days=7)
        assert resp.period_days == 7

    def test_get_image(self, client):
        resp = client.get_image(12345)
        assert resp.item_id == 12345

    def test_get_image_url(self, client):
        url = client.get_image_url(12345, format="hero")
        assert "cms.state-of.biz" in url

    def test_premium_search(self, client):
        resp = client.premium_search("ECB rate")
        assert resp.total == 1

    def test_premium_rag_context(self, client):
        resp = client.premium_rag_context("ECB policy", max_tokens=4000)
        assert resp.total_tokens_estimate == 500

    def test_get_briefing(self, client):
        resp = client.get_briefing(12345)
        assert resp.id == 12345
        assert resp.institution_code == "ECB"

    def test_get_image_feed(self, client):
        resp = client.get_image_feed()
        assert resp.total == 1

    def test_get_cross_institution(self, client):
        resp = client.get_cross_institution(["ECB", "FED"])
        assert resp.period_days == 7

    def test_get_weekly_digest(self, client):
        resp = client.get_weekly_digest()
        assert resp.period == "7 days"


class TestCredits:
    def test_get_balance(self, client):
        resp = client.get_balance()
        assert resp.balance == 850

    def test_get_balance_explicit_wallet(self, client):
        resp = client.get_balance(wallet="OtherWallet12345678901234567890123")
        assert resp.balance == 850

    def test_get_balance_no_wallet(self):
        c = SOBClient()
        with pytest.raises(ValueError, match="No wallet"):
            c.get_balance()

    def test_purchase_credits(self, client):
        resp = client.purchase_credits("TxSig123")
        assert resp.credits_granted == 1000

    def test_purchase_credits_no_wallet(self):
        c = SOBClient()
        with pytest.raises(ValueError, match="No wallet"):
            c.purchase_credits("TxSig123")


class TestErrorHandling:
    def test_402_payment_required(self, mock_402_transport):
        c = SOBClient(base_url="https://test.local")
        c._client = httpx.Client(transport=mock_402_transport, base_url="https://test.local")
        with pytest.raises(PaymentRequired) as exc_info:
            c.get_institutions()
        assert exc_info.value.credits_cost == 100
        assert exc_info.value.wallet == "TestWallet"

    def test_429_rate_limited(self, mock_429_transport):
        c = SOBClient(base_url="https://test.local")
        c._client = httpx.Client(transport=mock_429_transport, base_url="https://test.local")
        with pytest.raises(RateLimited) as exc_info:
            c.list_items()
        assert exc_info.value.retry_after == 60.0


class TestClientLifecycle:
    def test_context_manager(self, mock_transport):
        with SOBClient(base_url="https://test.local") as c:
            c._client = httpx.Client(transport=mock_transport, base_url="https://test.local")
            resp = c.list_items()
            assert resp.total == 1

    def test_headers_set(self):
        c = SOBClient(api_key="test-key", wallet="test-wallet")
        assert c._client.headers.get("X-API-Key") == "test-key"
        assert c._client.headers.get("X-Credits-Wallet") == "test-wallet"
        c.close()
