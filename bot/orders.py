"""
Order Placement Module
Handles placing Market and Limit orders on Binance Futures Testnet.
"""

import logging
from typing import Optional

from bot.client import get_client
from bot.validators import (
    ValidationError,
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
    validate_time_in_force,
)


logger = logging.getLogger("trading_bot")


def place_market_order(
    symbol: str,
    side: str,
    quantity: str,
    dry_run: bool = False,
) -> dict:
    """
    Place a market order on Binance Futures Testnet.

    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side - BUY or SELL
        quantity: Order quantity as string
        dry_run: If True, simulate order without sending to API

    Returns:
        Dict with order response data including orderId, status, executedQty, averagePrice

    Raises:
        ValidationError: If inputs are invalid
        RuntimeError: If order placement fails
    """
    logger.info("=== Market Order Request ===")
    logger.info("Symbol: %s | Side: %s | Quantity: %s", symbol, side, quantity)

    # Validate inputs
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    qty = validate_quantity(quantity)

    if dry_run:
        logger.info("DRY RUN - Order would be placed: %s %s %s", side, qty, symbol)
        return {
            "dry_run": True,
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": qty,
            "status": "DRY_RUN",
            "orderId": 0,
            "executedQty": 0,
            "avgPrice": 0.0,
        }

    # Place order
    try:
        client = get_client()
        logger.info("Sending MARKET order to Binance...")

        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=qty,
        )

        logger.info("Order placed successfully. Response: %s", response)

        return {
            "dry_run": False,
            "symbol": response.get("symbol", symbol),
            "side": response.get("side", side),
            "type": response.get("type", "MARKET"),
            "quantity": qty,
            "status": response.get("status", "UNKNOWN"),
            "orderId": response.get("orderId", 0),
            "clientOrderId": response.get("clientOrderId", ""),
            "executedQty": float(response.get("executedQty", 0)),
            "avgPrice": _safe_avg_price(response.get("avgPrice", 0)),
            "fills": response.get("fills", []),
            "updateTime": response.get("updateTime", 0),
        }

    except ValidationError:
        raise
    except Exception as e:
        logger.error("Failed to place market order: %s", e)
        raise RuntimeError(f"Failed to place market order. Reason: {e}") from e


def place_limit_order(
    symbol: str,
    side: str,
    quantity: str,
    price: str,
    time_in_force: str = "GTC",
    dry_run: bool = False,
) -> dict:
    """
    Place a limit order on Binance Futures Testnet.

    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side - BUY or SELL
        quantity: Order quantity as string
        price: Limit price as string
        time_in_force: Order duration (GTC, IOC, or FOK). Default: GTC
        dry_run: If True, simulate order without sending to API

    Returns:
        Dict with order response data including orderId, status, executedQty, price

    Raises:
        ValidationError: If inputs are invalid
        RuntimeError: If order placement fails
    """
    logger.info("=== Limit Order Request ===")
    logger.info(
        "Symbol: %s | Side: %s | Quantity: %s | Price: %s | TIF: %s",
        symbol, side, quantity, price, time_in_force,
    )

    # Validate inputs
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    qty = validate_quantity(quantity)
    p = validate_price(price)
    tif = validate_time_in_force(time_in_force)

    if dry_run:
        logger.info(
            "DRY RUN - Order would be placed: %s %s %s @ %s [%s]",
            side, qty, symbol, p, tif,
        )
        return {
            "dry_run": True,
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "quantity": qty,
            "price": p,
            "timeInForce": tif,
            "status": "DRY_RUN",
            "orderId": 0,
            "executedQty": 0,
            "avgPrice": 0.0,
        }

    # Place order
    try:
        client = get_client()
        logger.info("Sending LIMIT order to Binance...")

        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce=tif,
            quantity=qty,
            price=p,
        )

        logger.info("Order placed successfully. Response: %s", response)

        return {
            "dry_run": False,
            "symbol": response.get("symbol", symbol),
            "side": response.get("side", side),
            "type": response.get("type", "LIMIT"),
            "quantity": qty,
            "price": p,
            "timeInForce": tif,
            "status": response.get("status", "UNKNOWN"),
            "orderId": response.get("orderId", 0),
            "clientOrderId": response.get("clientOrderId", ""),
            "executedQty": float(response.get("executedQty", 0)),
            "avgPrice": _safe_avg_price(response.get("avgPrice", 0)),
            "fills": response.get("fills", []),
            "updateTime": response.get("updateTime", 0),
        }

    except ValidationError:
        raise
    except Exception as e:
        logger.error("Failed to place limit order: %s", e)
        raise RuntimeError(f"Failed to place limit order. Reason: {e}") from e


def _safe_avg_price(avg_price) -> float:
    """Safely convert avgPrice to float, handling string/None."""
    if avg_price is None:
        return 0.0
    try:
        return round(float(avg_price), 2)
    except (ValueError, TypeError):
        return 0.0
