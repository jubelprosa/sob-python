"""Exception classes for the SOB Python SDK."""

from __future__ import annotations

import base64
import json


class SOBError(Exception):
    """Base exception for SOB SDK errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class PaymentRequired(SOBError):
    """402 Payment Required.

    Raised when an endpoint requires payment. Contains parsed payment
    information from response headers.
    """

    def __init__(
        self,
        message: str,
        *,
        tier: int | None = None,
        credits_cost: int | None = None,
        credits_balance: int | None = None,
        wallet: str | None = None,
        network: str | None = None,
        payment_required: dict | None = None,
    ):
        super().__init__(message, status_code=402)
        self.tier = tier
        self.credits_cost = credits_cost
        self.credits_balance = credits_balance
        self.wallet = wallet
        self.network = network
        self.payment_required = payment_required

    @classmethod
    def from_response(cls, response) -> PaymentRequired:
        """Parse a 402 response into a PaymentRequired exception."""
        headers = response.headers

        # Parse credits info from headers
        credits_cost = _int_or_none(headers.get("X-Credits-Cost"))
        credits_balance = _int_or_none(headers.get("X-Credits-Balance"))
        credits_required = _int_or_none(headers.get("X-Credits-Required"))
        wallet = headers.get("X-Wallet")
        network = headers.get("X-Network")

        # Parse x402 payment-required header (Base64-encoded JSON)
        payment_required = None
        pr_header = headers.get("payment-required")
        if pr_header:
            try:
                payment_required = json.loads(base64.b64decode(pr_header).decode())
            except Exception:
                pass

        # Determine tier from payment_required or credits cost
        tier = None
        if payment_required:
            from sob._constants import TIER_USDC_ATOMIC

            amount = payment_required.get("maxAmountRequired")
            if amount:
                for t, cost in TIER_USDC_ATOMIC.items():
                    if str(cost) == str(amount):
                        tier = t
                        break

        # Use credits_required as fallback for balance display
        effective_cost = credits_cost or credits_required

        # Build message
        detail = _get_json_detail(response)
        msg = detail or "Payment Required"
        if effective_cost:
            msg = f"Payment Required: {effective_cost} credits"
            if credits_balance is not None:
                msg += f" (balance: {credits_balance})"

        return cls(
            msg,
            tier=tier,
            credits_cost=effective_cost,
            credits_balance=credits_balance,
            wallet=wallet,
            network=network,
            payment_required=payment_required,
        )


class RateLimited(SOBError):
    """429 Too Many Requests."""

    def __init__(self, message: str, retry_after: float | None = None):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after

    @classmethod
    def from_response(cls, response) -> RateLimited:
        """Parse a 429 response into a RateLimited exception."""
        retry_after = None
        ra = response.headers.get("Retry-After")
        if ra:
            try:
                retry_after = float(ra)
            except ValueError:
                pass

        detail = _get_json_detail(response)
        msg = detail or "Rate limit exceeded"
        if retry_after:
            msg += f" (retry after {retry_after}s)"

        return cls(msg, retry_after=retry_after)


class NotFound(SOBError):
    """404 Not Found."""

    def __init__(self, message: str = "Not found"):
        super().__init__(message, status_code=404)

    @classmethod
    def from_response(cls, response) -> NotFound:
        detail = _get_json_detail(response)
        return cls(detail or "Not found")


class AuthenticationError(SOBError):
    """401 Unauthorized."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, status_code=401)


class BadRequest(SOBError):
    """400 Bad Request."""

    def __init__(self, message: str = "Bad request"):
        super().__init__(message, status_code=400)

    @classmethod
    def from_response(cls, response) -> BadRequest:
        detail = _get_json_detail(response)
        return cls(detail or "Bad request")


class ServerError(SOBError):
    """5xx Server Error."""

    def __init__(self, message: str = "Server error", status_code: int = 500):
        super().__init__(message, status_code=status_code)

    @classmethod
    def from_response(cls, response) -> ServerError:
        detail = _get_json_detail(response)
        return cls(detail or "Server error", status_code=response.status_code)


def _int_or_none(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _get_json_detail(response) -> str | None:
    try:
        data = response.json()
        if isinstance(data, dict):
            return data.get("detail")
    except Exception:
        pass
    return None
