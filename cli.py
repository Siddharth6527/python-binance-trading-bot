"""
CLI Application for Trading Bot
Uses Typer for command-line interface and Rich for terminal output.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import print as rprint

from bot.logging_config import setup_logging
from bot.orders import place_limit_order, place_market_order


app = typer.Typer(
    name="trading-bot",
    help="CLI tool to place Market and Limit orders on Binance Futures Testnet.",
    add_completion=False,
)

console = Console()


def print_banner() -> None:
    """Print application banner."""
    banner = """
[bold cyan]╔══════════════════════════════════════╗[/bold cyan]
[bold cyan]║   🚀 Binance Futures Trading Bot    ║[/bold cyan]
[bold cyan]║         Testnet Edition             ║[/bold cyan]
[bold cyan]╚══════════════════════════════════════╝[/bold cyan]
"""
    console.print(banner)


def print_order_summary(result: dict) -> None:
    """Print a formatted order summary."""
    is_dry_run = result.get("dry_run", False)
    status_icon = "⚠️" if is_dry_run else "✅"
    status_text = "DRY RUN" if is_dry_run else "SUCCESS"

    # Build summary text
    lines = []
    lines.append(f"[bold]Symbol:[/bold]       {result.get('symbol', 'N/A')}")
    lines.append(f"[bold]Side:[/bold]         {result.get('side', 'N/A')}")
    lines.append(f"[bold]Type:[/bold]         {result.get('type', 'N/A')}")
    lines.append(f"[bold]Quantity:[/bold]     {result.get('quantity', 'N/A')}")

    if result.get("type") == "LIMIT":
        lines.append(f"[bold]Price:[/bold]        {result.get('price', 'N/A')}")
        lines.append(f"[bold]Time in Force:[/bold] {result.get('timeInForce', 'GTC')}")

    lines.append(f"")
    lines.append(f"[bold]{status_icon} Status:[/bold]    [green]{status_text}[/green]")
    lines.append(f"[bold]Order ID:[/bold]    {result.get('orderId', 'N/A')}")

    if not is_dry_run:
        executed = result.get("executedQty", 0)
        avg_price = result.get("avgPrice", 0)
        if executed and executed > 0:
            lines.append(f"[bold]Executed:[/bold]    {executed}")
        if avg_price and avg_price > 0:
            lines.append(f"[bold]Avg Price:[/bold]   {avg_price}")

    summary = "\n".join(lines)

    if is_dry_run:
        panel = Panel(summary, title="[bold yellow]Order Summary (Dry Run)[/bold yellow]", border_style="yellow")
    else:
        panel = Panel(summary, title="[bold green]Order Summary[/bold green]", border_style="green")

    console.print(panel)


def print_error(title: str, message: str) -> None:
    """Print a formatted error message."""
    error_text = Text(message, style="bold red")
    console.print(Panel(error_text, title=f"[bold red]{title}[/bold red]", border_style="red"))


@app.command()
def market(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair (e.g., BTCUSDT)"),
    side: str = typer.Option(..., "--side", "-d", help="Order side: BUY or SELL"),
    quantity: str = typer.Option(..., "--quantity", "-q", help="Order quantity"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate order without sending to API"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
) -> None:
    """
    Place a MARKET order on Binance Futures Testnet.
    """
    # Setup logging
    log_level = "DEBUG" if verbose else "INFO"
    setup_logging(log_level=log_level)

    print_banner()

    try:
        result = place_market_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            dry_run=dry_run,
        )
        print_order_summary(result)

    except ValidationError as e:
        logger.error("Validation error: %s", e)
        print_error("Validation Error", str(e))
        raise typer.Exit(code=1)
    except RuntimeError as e:
        logger.error("Runtime error: %s", e)
        print_error("Order Failed", str(e))
        raise typer.Exit(code=1)
    except ValueError as e:
        logger.error("Configuration error: %s", e)
        print_error("Configuration Error", str(e))
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error("Unexpected error: %s", e, exc_info=True)
        print_error("Unexpected Error", f"{e}")
        raise typer.Exit(code=1)


@app.command()
def limit(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair (e.g., BTCUSDT)"),
    side: str = typer.Option(..., "--side", "-d", help="Order side: BUY or SELL"),
    quantity: str = typer.Option(..., "--quantity", "-q", help="Order quantity"),
    price: str = typer.Option(..., "--price", "-p", help="Limit price"),
    time_in_force: str = typer.Option("GTC", "--time-in-force", "-t", help="Time in force: GTC, IOC, FOK"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate order without sending to API"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
) -> None:
    """
    Place a LIMIT order on Binance Futures Testnet.
    """
    # Setup logging
    log_level = "DEBUG" if verbose else "INFO"
    setup_logging(log_level=log_level)

    print_banner()

    try:
        result = place_limit_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
            dry_run=dry_run,
        )
        print_order_summary(result)

    except ValidationError as e:
        logger.error("Validation error: %s", e)
        print_error("Validation Error", str(e))
        raise typer.Exit(code=1)
    except RuntimeError as e:
        logger.error("Runtime error: %s", e)
        print_error("Order Failed", str(e))
        raise typer.Exit(code=1)
    except ValueError as e:
        logger.error("Configuration error: %s", e)
        print_error("Configuration Error", str(e))
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error("Unexpected error: %s", e, exc_info=True)
        print_error("Unexpected Error", f"{e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
