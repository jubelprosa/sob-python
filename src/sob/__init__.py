"""SOB Python SDK — Central bank intelligence API client.

Usage:
    from sob import SOBClient

    client = SOBClient()
    items = client.list_items()

    # With premium access
    client = SOBClient(wallet="YourSolanaWallet...")
    rates = client.get_rates()

    # Async
    from sob import AsyncSOBClient

    async with AsyncSOBClient() as client:
        items = await client.list_items()
"""

__version__ = "1.0.0"

from sob.client import AsyncSOBClient, SOBClient
from sob.exceptions import (
    AuthenticationError,
    BadRequest,
    NotFound,
    PaymentRequired,
    RateLimited,
    ServerError,
    SOBError,
)

__all__ = [
    "SOBClient",
    "AsyncSOBClient",
    "SOBError",
    "PaymentRequired",
    "RateLimited",
    "NotFound",
    "AuthenticationError",
    "BadRequest",
    "ServerError",
    "__version__",
]
