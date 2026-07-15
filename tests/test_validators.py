"""
Tests for Trading Bot Validators
"""

import pytest
from bot.validators import (
    ValidationError,
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
    validate_time_in_force,
)


class TestValidateSymbol:
    def test_valid_symbol(self):
        assert validate_symbol("BTCUSDT") == "BTCUSDT"

    def test_valid_symbol_lowercase(self):
        assert validate_symbol("btcusdt") == "BTCUSDT"

    def test_valid_symbol_mixed_case(self):
        assert validate_symbol("BtcUsdt") == "BTCUSDT"

    def test_symbol_with_whitespace(self):
        assert validate_symbol("  BTCUSDT  ") == "BTCUSDT"

    def test_symbol_too_short(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_symbol("ABC")
        assert "length" in str(exc_info.value).lower()

    def test_symbol_empty(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_symbol("")
        assert "empty" in str(exc_info.value).lower()

    def test_symbol_none(self):
        with pytest.raises(ValidationError):
            validate_symbol(None)

    def test_symbol_with_special_chars(self):
        with pytest.raises(ValidationError):
            validate_symbol("BTC-ETH")


class TestValidateSide:
    def test_buy(self):
        assert validate_side("BUY") == "BUY"

    def test_sell(self):
        assert validate_side("SELL") == "SELL"

    def test_lowercase(self):
        assert validate_side("buy") == "BUY"
        assert validate_side("sell") == "SELL"

    def test_invalid_side(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_side("HOLD")
        assert "BUY or SELL" in str(exc_info.value)

    def test_empty_side(self):
        with pytest.raises(ValidationError):
            validate_side("")


class TestValidateQuantity:
    def test_valid_quantity(self):
        assert validate_quantity("0.01") == 0.01

    def test_integer_quantity(self):
        assert validate_quantity("1") == 1.0

    def test_quantity_zero(self):
        with pytest.raises(ValidationError):
            validate_quantity("0")

    def test_quantity_negative(self):
        with pytest.raises(ValidationError):
            validate_quantity("-0.01")

    def test_quantity_not_number(self):
        with pytest.raises(ValidationError):
            validate_quantity("abc")

    def test_quantity_none(self):
        with pytest.raises(ValidationError):
            validate_quantity(None)


class TestValidatePrice:
    def test_valid_price(self):
        assert validate_price("50000.00") == 50000.0

    def test_price_zero(self):
        with pytest.raises(ValidationError):
            validate_price("0")

    def test_price_negative(self):
        with pytest.raises(ValidationError):
            validate_price("-100")

    def test_price_not_number(self):
        with pytest.raises(ValidationError):
            validate_price("abc")

    def test_price_none(self):
        with pytest.raises(ValidationError):
            validate_price(None)


class TestValidateOrderType:
    def test_market(self):
        assert validate_order_type("MARKET") == "MARKET"

    def test_limit(self):
        assert validate_order_type("LIMIT") == "LIMIT"

    def test_lowercase(self):
        assert validate_order_type("market") == "MARKET"

    def test_invalid_type(self):
        with pytest.raises(ValidationError):
            validate_order_type("STOP")


class TestValidateTimeInForce:
    def test_gtc(self):
        assert validate_time_in_force("GTC") == "GTC"

    def test_ioc(self):
        assert validate_time_in_force("IOC") == "IOC"

    def test_fok(self):
        assert validate_time_in_force("FOK") == "FOK"

    def test_default_empty(self):
        assert validate_time_in_force("") == "GTC"

    def test_invalid_tif(self):
        with pytest.raises(ValidationError):
            validate_time_in_force("DAY")
