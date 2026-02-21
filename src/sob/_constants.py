"""Constants for the SOB Python SDK."""

BASE_URL = "https://state-of.biz"

# Header names
HEADER_API_KEY = "X-API-Key"
HEADER_CREDITS_WALLET = "X-Credits-Wallet"
HEADER_PAYMENT = "X-Payment"
HEADER_PAYMENT_SIGNATURE = "payment-signature"

# 402 response headers
HEADER_CREDITS_COST = "X-Credits-Cost"
HEADER_CREDITS_BALANCE = "X-Credits-Balance"
HEADER_CREDITS_REQUIRED = "X-Credits-Required"
HEADER_CREDITS_PER_SOL = "X-Credits-Per-Sol"
HEADER_WALLET = "X-Wallet"
HEADER_NETWORK = "X-Network"
HEADER_PAYMENT_REQUIRED = "payment-required"
HEADER_PRICE = "X-Price"
HEADER_RETRY_AFTER = "Retry-After"

# Credit system
CREDITS_PER_SOL = 1_000_000

# Tier costs (credits per request)
TIER_COSTS = {
    1: 1,       # Metadata
    2: 10,      # Structured data
    3: 100,     # Semantic objects
    4: 1_000,   # Composite reports
}

# USDC atomic units per tier
TIER_USDC_ATOMIC = {
    1: 10,       # $0.00001
    2: 100,      # $0.0001
    3: 1_000,    # $0.001
    4: 10_000,   # $0.01
}
