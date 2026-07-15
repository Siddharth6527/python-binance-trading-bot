"""
Tests for Trading Bot Orders Module
"""

import pytest
from unittest.mock import patch, MagicMock
from bot.orders import place_market_order, place_limit_order
from bot.validators import ValidationError


class TestPlaceMarketOrder:
    @patch("bot.orders.get_client")
    def test_place_market_order_success(self, mock_get_client):
        """Test successful market order placement."""
        mock_client = MagicMock()
        mock_client.futures_create_order.return_value = {
            "symbol": "BTCUSDT",
            "orderId": 123456,
            "clientOrderId": "test-order-id",
            "transactTime": 1234567890000,
            "price": "0.00000000",
            "origQty": "0.001",
            "executedQty": "0.001",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "BUY",
            "avgPrice": "50000.00",
        }
        mock_get_client.return_value = mock_client

        result = place_market_order("BTCUSDT", "BUY", "0.001")

        assert result["symbol"] == "BTCUSDT"
        assert result["side"] == "BUY"
        assert result["type"] == "MARKET"
        assert result["orderId"] == 123456
        assert result["status"] == "FILLED"

    @patch("bot.orders.get_client")
    def test_place_market_order_dry_run(self, mock_get_client):
        """Test market order dry run."""
        result = place_market_order("BTCUSDT", "BUY", "0.001", dry_run=True)

        assert result["dry_run"] is True
        assert result["status"] == "DRY_RUN"
        mock_get_client.assert_not_called()

    def test_place_market_order_invalid_symbol(self):
        """Test market order with invalid symbol."""
        with pytest.raises(ValidationError):
            place_market_order("", "BUY", "0.001")

    def test_place_market_order_invalid_side(self):
        """Test market order with invalid side."""
        with pytest.raises(ValidationError):
            place_market_order("BTCUSDT", "HOLD", "0.001")

    def test_place_market_order_invalid_quantity(self):
        """Test market order with invalid quantity."""
        with pytest.raises(ValidationError):
            place_market_order("BTCUSDT", "BUY", "0")


class TestPlaceLimitOrder:
    @patch("bot.orders.get_client")
    def test_place_limit_order_success(self, mock_get_client):
        """Test successful limit order placement."""
        mock_client = MagicMock()
        mock_client.futures_create_order.return_value = {
            "symbol": "BTCUSDT",
            "orderId": 789012,
            "clientOrderId": "test-limit-id",
            "transactTime": 1234567890000,
            "price": "48000.00",
            "origQty": "0.001",
            "executedQty": "0",
            "status": "NEW",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "SELL",
        }
        mock_get_client.return_value = mock_client

        result = place_limit_order("BTCUSDT", "SELL", "0.001", "48000.00")

        assert result["symbol"] == "BTCUSDT"
        assert result["side"] == "SELL"
        assert result["type"] == "LIMIT"
        assert result["price"] == 48000.0
        assert result["orderId"] == 789012
        assert result["status"] == "NEW"

    @patch("bot.orders.get_client")
    def test_place_limit_order_dry_run(self, mock_get_client):
        """Test limit order dry run."""
        result = place_limit_order("BTCUSDT", "SELL", "0.001", "48000.00", dry_run=True)

        assert result["dry_run"] is True
        assert result["status"] == "DRY_RUN"
        assert result["price"] == 48000.0
        mock_get_client.assert_not_called()

    def test_place_limit_order_invalid_price(self):
        """Test limit order with invalid price."""
        with pytest.raises(ValidationError):
            place_limit_order("BTCUSDT", "BUY", "0.001", "-100")

    def test_place_limit_order_missing_price(self):
        """Test limit order with missing price."""
        with pytest.raises(ValidationError):
            place_limit_order("BTCUSDT", "BUY", "0.001", None)

    def test_place_limit_order_ioc(self):
        """Test limit order with IOC time in force."""
        mock_client = MagicMock()
        mock_client.futures_create_order.return_value = {
            "symbol": "BTCUSDT",
            "orderId": 999,
            "executedQty": "0",
            "status": "NEW",
            "avgPrice": "0",
        }

        with patch("bot.orders.get_client", return_value=mock_client):
            result = place_limit_order(
                "BTCUSDT", "BUY", "0.001", "50000",
                time_in_force="IOC",
            )
            assert result["timeInForce"] == "IOC"
