"""Tests for exception parsing from HTTP responses."""

import base64
import json

import httpx

from sob.exceptions import (
    BadRequest,
    NotFound,
    PaymentRequired,
    RateLimited,
    ServerError,
    SOBError,
)


def test_sob_error_base():
    err = SOBError("test", status_code=500)
    assert str(err) == "test"
    assert err.status_code == 500


def test_payment_required_from_402_with_headers():
    payment_req = {
        "scheme": "exact",
        "network": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
        "maxAmountRequired": "1000",
        "resource": "https://state-of.biz/api/premium/semantic-search",
        "payTo": "TestPayTo",
        "asset": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    }
    response = httpx.Response(
        402,
        json={"detail": "Payment Required"},
        headers={
            "X-Credits-Cost": "100",
            "X-Credits-Per-Sol": "1000000",
            "X-Wallet": "WalletABC",
            "X-Network": "devnet",
            "payment-required": base64.b64encode(json.dumps(payment_req).encode()).decode(),
        },
    )
    err = PaymentRequired.from_response(response)
    assert err.status_code == 402
    assert err.credits_cost == 100
    assert err.wallet == "WalletABC"
    assert err.network == "devnet"
    assert err.payment_required is not None
    assert err.payment_required["maxAmountRequired"] == "1000"
    assert err.tier == 3  # 1000 atomic = Tier 3


def test_payment_required_insufficient_credits():
    response = httpx.Response(
        402,
        json={"detail": "Insufficient credits"},
        headers={
            "X-Credits-Required": "100",
            "X-Credits-Balance": "42",
            "X-Credits-Per-Sol": "1000000",
            "X-Wallet": "WalletABC",
            "X-Network": "mainnet-beta",
        },
    )
    err = PaymentRequired.from_response(response)
    assert err.credits_cost == 100
    assert err.credits_balance == 42
    assert "100 credits" in str(err)
    assert "balance: 42" in str(err)


def test_payment_required_minimal():
    response = httpx.Response(402, json={"detail": "Payment Required"})
    err = PaymentRequired.from_response(response)
    assert err.status_code == 402
    assert err.credits_cost is None
    assert err.payment_required is None


def test_rate_limited_with_retry_after():
    response = httpx.Response(
        429,
        json={"detail": "Rate limit exceeded"},
        headers={"Retry-After": "30"},
    )
    err = RateLimited.from_response(response)
    assert err.status_code == 429
    assert err.retry_after == 30.0
    assert "retry after 30.0s" in str(err)


def test_rate_limited_without_retry_after():
    response = httpx.Response(429, json={"detail": "Too many requests"})
    err = RateLimited.from_response(response)
    assert err.retry_after is None
    assert "Too many requests" in str(err)


def test_not_found():
    response = httpx.Response(404, json={"detail": "Item not found"})
    err = NotFound.from_response(response)
    assert err.status_code == 404
    assert "Item not found" in str(err)


def test_bad_request():
    response = httpx.Response(400, json={"detail": "Invalid wallet"})
    err = BadRequest.from_response(response)
    assert err.status_code == 400
    assert "Invalid wallet" in str(err)


def test_server_error():
    response = httpx.Response(503, json={"detail": "Service unavailable"})
    err = ServerError.from_response(response)
    assert err.status_code == 503
    assert "Service unavailable" in str(err)


def test_payment_required_bad_base64_header():
    """Gracefully handle malformed payment-required header."""
    response = httpx.Response(
        402,
        json={"detail": "Payment Required"},
        headers={"payment-required": "not-valid-base64!!!"},
    )
    err = PaymentRequired.from_response(response)
    assert err.payment_required is None  # Failed to parse, but no crash
