"""
Binance Client Module
Handles connection to Binance Futures Testnet API.
"""

import os
from typing import Optional

from binance.client import Client
from binance.enums import FuturesType

from bot.logging_config import logger


def get_client(api_key: Optional[str] = None, api_secret: Optional[str] = None) -> Client:
    """
    Create and return an authenticated Binance Futures client.

    Reads credentials from environment variables if not provided explicitly.

    Args:
        api_key: Binance API key
        api_secret: Binance API secret

    Returns:
        Authenticated Binance Client instance configured for Futures

    Raises:
        ValueError: If API credentials are missing
    """
    key = api_key or os.getenv("BINANCE_API_KEY", "")
    secret = api_secret or os.getenv("BINANCE_API_SECRET", "")

    if not key or not secret:
        raise ValueError(
            "Missing Binance API credentials. "
            "Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables, "
            "or pass them as arguments."
        )

    logger.info("Creating Binance Futures client...")

    # Create client
    client = Client(key, secret)

    # Verify connection
    try:
        # Test connection by fetching server time
        client.futures_time()
        logger.info("Successfully connected to Binance Futures API.")
    except Exception as e:
        logger.error("Failed to connect to Binance API: %s", e)
        raise ConnectionError(
            f"Failed to connect to Binance API. "
            f"Check your API credentials and internet connection. "
            f"Error: {e}"
        ) from e

    return client


def get_testnet_url() -> str:
    """
    Return the Binance Futures Testnet base URL.

    Returns:
        Testnet base URL string
    """
    return "https://testnet.binancefuture.com"
