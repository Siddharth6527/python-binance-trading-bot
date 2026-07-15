# 🚀 Binance Futures Testnet Trading Bot

A Python CLI application that places **Market** and **Limit** orders on the **Binance Futures Testnet** with clean architecture, validation, logging, and exception handling.

## ✨ Features

- 📈 **Market Orders** — Instant execution at current market price
- 🎯 **Limit Orders** — Execute at a specific price (GTC, IOC, FOK)
- ✅ **Input Validation** — All inputs validated before hitting the API
- 📋 **Structured Logging** — File + console logging with rotation
- 🛡️ **Exception Handling** — Graceful error handling for all failure modes
- 🔍 **Dry Run Mode** — Test without placing real orders
- 🎨 **Beautiful CLI** — Formatted output with Rich library
- 🧪 **Tests** — Unit tests for validators and order logic

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.9+ |
| CLI | Typer |
| Terminal Output | Rich |
| Binance API | python-binance |
| Config | python-dotenv |
| Testing | pytest |

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- A Binance Futures Testnet account

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd python-binance-trading-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configure API Keys

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Create an account and generate API key + secret
3. Enable Futures permissions on your API key
4. Copy `.env.example` to `.env` and add your keys:

```bash
cp .env.example .env
```

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
USE_TESTNET=True
```

## 🏗 Project Structure

```
trading-bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API connection
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── logs/
│   └── bot.log            # Application logs
├── tests/
│   ├── test_validators.py # Validator tests
│   └── test_orders.py     # Order tests
├── cli.py                 # CLI entry point
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Usage

### Market Order

```bash
# Place a market buy order
python cli.py market --symbol BTCUSDT --side BUY --quantity 0.01

# Place a market sell order
python cli.py market --symbol ETHUSDT --side SELL --quantity 0.1

# Dry run (no actual order)
python cli.py market --symbol BTCUSDT --side BUY --quantity 0.01 --dry-run
```

### Limit Order

```bash
# Place a limit buy order at $50,000
python cli.py limit --symbol BTCUSDT --side BUY --quantity 0.01 --price 50000

# Place a limit sell order with IOC (Immediate or Cancel)
python cli.py limit --symbol ETHUSDT --side SELL --quantity 0.1 --price 3000 --time-in-force IOC
```

### Verbose Mode

```bash
python cli.py market --symbol BTCUSDT --side BUY --quantity 0.01 --verbose
```

## 📝 CLI Reference

### `market` — Place a Market Order

| Option | Required | Description |
|--------|----------|-------------|
| `-s, --symbol` | ✅ | Trading pair (e.g., BTCUSDT) |
| `-d, --side` | ✅ | Order side: BUY or SELL |
| `-q, --quantity` | ✅ | Order quantity |
| `--dry-run` | ❌ | Simulate without sending to API |
| `-v, --verbose` | ❌ | Enable debug logging |

### `limit` — Place a Limit Order

| Option | Required | Description |
|--------|----------|-------------|
| `-s, --symbol` | ✅ | Trading pair (e.g., BTCUSDT) |
| `-d, --side` | ✅ | Order side: BUY or SELL |
| `-q, --quantity` | ✅ | Order quantity |
| `-p, --price` | ✅ | Limit price |
| `-t, --time-in-force` | ❌ | GTC, IOC, or FOK (default: GTC) |
| `--dry-run` | ❌ | Simulate without sending to API |
| `-v, --verbose` | ❌ | Enable debug logging |

## ✅ Validation Rules

- **Symbol**: 6-20 characters, alphanumeric only, auto-uppercased
- **Side**: Must be `BUY` or `SELL` (case-insensitive)
- **Quantity**: Must be a number > 0
- **Price**: Must be a number > 0 (required for limit orders)
- **Time in Force**: Must be `GTC`, `IOC`, or `FOK`

## 🔍 Logging

All actions are logged to `logs/bot.log` with timestamps and severity levels:

- ✅ Application start / connection events
- 📤 API requests sent
- 📥 API responses received
- ❌ Errors (network, API, validation)
- 🛡️ Retry attempts

## 🧪 Running Tests

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=bot --cov-report=term-missing
```

## 🏗 Architecture

The project follows **separation of concerns**:

| Module | Responsibility |
|--------|---------------|
| `cli.py` | User interface, argument parsing, output formatting |
| `bot/orders.py` | Order placement logic, response parsing |
| `bot/validators.py` | Input validation, error messages |
| `bot/client.py` | API authentication and connection |
| `bot/logging_config.py` | Logging configuration |

## ⚠️ Important Notes

- This bot uses the **Binance Futures Testnet** only. Do not use with real funds.
- The `.env` file is **not** committed to version control.
- API keys stored in `.env` are never exposed in logs.
- Order responses include `executedQty` and `avgPrice` for verification.

## 📚 Learning Objectives

This project demonstrates:

- ✅ Clean Python architecture (single responsibility per module)
- ✅ Type hints and docstrings
- ✅ Input validation with custom exceptions
- ✅ Structured logging with rotation
- ✅ CLI development with Typer
- ✅ Beautiful terminal output with Rich
- ✅ Exception handling and error reporting
- ✅ Unit testing with pytest
- ✅ Configuration management with dotenv

## 👨‍💻 Author

Built as a portfolio project demonstrating professional Python backend development practices.

---

*Built with Python, Typer, python-binance, and Rich*
