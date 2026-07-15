"""
Input Validation for Trading Bot
Validates all user inputs before sending orders to Binance.
"""

from typing import Optional


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}
VALID_TIME_IN_FORCE = {"GTC", "IOC", "FOK"}


class ValidationError(Exception):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        super().__init__(message)


def validate_symbol(symbol: str) -> str:
    """
    Validate trading pair symbol.

    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)

    Returns:
        Uppercase symbol string

    Raises:
        ValidationError: If symbol is invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol cannot be empty.", field="symbol")

    symbol = symbol.strip().upper()

    if len(symbol) < 6 or len(symbol) > 20:
        raise ValidationError(
            f"Invalid symbol length: '{symbol}'. Must be 6-20 characters.",
            field="symbol",
        )

    if not all(c.isalnum() for c in symbol):
        raise ValidationError(
            f"Invalid symbol: '{symbol}'. Must contain only letters and numbers.",
            field="symbol",
        )

    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side.

    Args:
        side: Order side (BUY or SELL)

    Returns:
        Uppercase side string

    Raises:
        ValidationError: If side is not BUY or SELL
    """
    if not side or not isinstance(side, str):
        raise ValidationError("Order side cannot be empty.", field="side")

    side = side.strip().upper()

    if side not in VALID_SIDES:
        raise ValidationError(
            f"Invalid order side: '{side}'. Must be BUY or SELL.",
            field="side",
        )

    return side


def validate_quantity(quantity: str, min_quantity: float = 0.0001) -> float:
    """
    Validate order quantity.

    Args:
        quantity: Quantity string to validate
        min_quantity: Minimum allowed quantity

    Returns:
        Float quantity value

    Raises:
        ValidationError: If quantity is invalid
    """
    if quantity is None:
        raise ValidationError("Quantity is required.", field="quantity")

    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(
            f"Invalid quantity: '{quantity}'. Must be a number.",
            field="quantity",
        )

    if qty <= 0:
        raise ValidationError(
            f"Quantity must be greater than 0. Got: {qty}",
            field="quantity",
        )

    if qty < min_quantity:
        raise ValidationError(
            f"Quantity {qty} is below minimum ({min_quantity}).",
            field="quantity",
        )

    return round(qty, 8)


def validate_price(price: str) -> float:
    """
    Validate limit order price.

    Args:
        price: Price string to validate

    Returns:
        Float price value

    Raises:
        ValidationError: If price is invalid
    """
    if price is None:
        raise ValidationError("Price is required for limit orders.", field="price")

    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValidationError(
            f"Invalid price: '{price}'. Must be a number.",
            field="price",
        )

    if p <= 0:
        raise ValidationError(
            f"Price must be greater than 0. Got: {p}",
            field="price",
        )

    return round(p, 2)


def validate_order_type(order_type: str) -> str:
    """
    Validate order type.

    Args:
        order_type: Order type (MARKET or LIMIT)

    Returns:
        Uppercase order type string

    Raises:
        ValidationError: If order type is invalid
    """
    if not order_type or not isinstance(order_type, str):
        raise ValidationError("Order type cannot be empty.", field="order_type")

    order_type = order_type.strip().upper()

    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type: '{order_type}'. Must be MARKET or LIMIT.",
            field="order_type",
        )

    return order_type


def validate_time_in_force(time_in_force: str) -> str:
    """
    Validate time in force parameter.

    Args:
        time_in_force: Time in force (GTC, IOC, or FOK)

    Returns:
        Uppercase time in force string

    Raises:
        ValidationError: If time in force is invalid
    """
    if not time_in_force:
        return "GTC"  # Default

    time_in_force = time_in_force.strip().upper()

    if time_in_force not in VALID_TIME_IN_FORCE:
        raise ValidationError(
            f"Invalid time_in_force: '{time_in_force}'. Must be GTC, IOC, or FOK.",
            field="time_in_force",
        )

    return time_in_force
