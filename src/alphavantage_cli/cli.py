"""Command-line interface for Alpha Vantage CLI."""

import sys
import json
from pathlib import Path
from typing import Optional

import click

from .client import AlphaVantageClient
from .exceptions import AlphaVantageError, APIKeyError, RateLimitError
from .endpoints.indicators import IndicatorsEndpoint


def get_client(ctx):
    """Create client from deferred parameters."""
    try:
        return AlphaVantageClient(
            api_key=ctx.obj['api_key'],
            config_file=ctx.obj['config_file'],
            rate_limit_delay=ctx.obj['rate_limit_delay']
        )
    except APIKeyError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("\nTo get an API key, visit: https://www.alphavantage.co/support/#api-key", err=True)
        sys.exit(1)
    except AlphaVantageError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.group()
@click.option(
    "--api-key",
    envvar="ALPHA_VANTAGE_API_KEY",
    help="Alpha Vantage API key (can also set ALPHA_VANTAGE_API_KEY env var)"
)
@click.option(
    "--config-file",
    type=click.Path(exists=True),
    help="Path to configuration file"
)
@click.option(
    "--rate-limit",
    type=float,
    default=12.0,
    help="Rate limit delay in seconds (default: 12s for free tier)"
)
@click.pass_context
def cli(ctx, api_key: Optional[str], config_file: Optional[str], rate_limit: float):
    """Alpha Vantage CLI - Access financial market data from the command line."""
    # Store connection parameters for deferred client creation
    ctx.ensure_object(dict)
    ctx.obj = {
        'api_key': api_key,
        'config_file': config_file,
        'rate_limit_delay': rate_limit
    }


@cli.command()
@click.argument("symbol")
@click.option(
    "--output-format",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Output format"
)
@click.pass_context
def get_quote(ctx, symbol: str, output_format: str):
    """Get real-time stock quote."""
    client = get_client(ctx)
    try:
        data = client.stocks.get_quote(symbol, output_format)
        
        if output_format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            click.echo(data)
            
    except AlphaVantageError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("symbol")
@click.option(
    "--adjusted/--no-adjusted",
    default=True,
    help="Whether to return adjusted data"
)
@click.option(
    "--output-format",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Output format"
)
@click.option(
    "--outputsize",
    type=click.Choice(["compact", "full"]),
    default="compact",
    help="Data size (compact=latest 100 points, full=all available)"
)
@click.pass_context
def get_daily(
    ctx,
    symbol: str,
    adjusted: bool,
    output_format: str,
    outputsize: str
):
    """Get daily time series data."""
    client = get_client(ctx)
    try:
        data = client.stocks.get_daily(
            symbol,
            adjusted=adjusted,
            output_format=output_format,
            outputsize=outputsize
        )
        
        if output_format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            click.echo(data)
            
    except AlphaVantageError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("symbol")
@click.option(
    "--interval",
    type=click.Choice(["1min", "5min", "15min", "30min", "60min"]),
    default="5min",
    help="Time interval"
)
@click.option(
    "--adjusted/--no-adjusted",
    default=True,
    help="Whether to return adjusted data"
)
@click.option(
    "--output-format",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Output format"
)
@click.option(
    "--outputsize",
    type=click.Choice(["compact", "full"]),
    default="compact",
    help="Data size"
)
@click.pass_context
def get_intraday(
    ctx,
    symbol: str,
    interval: str,
    adjusted: bool,
    output_format: str,
    outputsize: str
):
    """Get intraday time series data."""
    client = get_client(ctx)
    try:
        data = client.stocks.get_intraday(
            symbol,
            interval=interval,
            adjusted=adjusted,
            output_format=output_format,
            outputsize=outputsize
        )
        
        if output_format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            click.echo(data)
            
    except AlphaVantageError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("symbol")
@click.option(
    "--indicator",
    required=True,
    help="Technical indicator (e.g., SMA, EMA, RSI, MACD, BBANDS)"
)
@click.option(
    "--interval",
    type=click.Choice(["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"]),
    default="daily",
    help="Time interval"
)
@click.option(
    "--time-period",
    type=int,
    default=20,
    help="Time period for calculation"
)
@click.option(
    "--series-type",
    type=click.Choice(["close", "open", "high", "low"]),
    default="close",
    help="Price series type"
)
@click.option(
    "--output-format",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Output format"
)
@click.pass_context
def get_indicators(
    ctx,
    symbol: str,
    indicator: str,
    interval: str,
    time_period: int,
    series_type: str,
    output_format: str
):
    """Get technical indicators."""
    client = get_client(ctx)
    try:
        # Map common indicators to their specific methods
        indicator_upper = indicator.upper()
        
        if indicator_upper == "SMA":
            data = client.indicators.get_sma(
                symbol,
                interval=interval,
                time_period=time_period,
                series_type=series_type,
                output_format=output_format
            )
        elif indicator_upper == "EMA":
            data = client.indicators.get_ema(
                symbol,
                interval=interval,
                time_period=time_period,
                series_type=series_type,
                output_format=output_format
            )
        elif indicator_upper == "RSI":
            data = client.indicators.get_rsi(
                symbol,
                interval=interval,
                time_period=time_period,
                series_type=series_type,
                output_format=output_format
            )
        elif indicator_upper == "MACD":
            data = client.indicators.get_macd(
                symbol,
                interval=interval,
                series_type=series_type,
                output_format=output_format
            )
        elif indicator_upper == "BBANDS":
            data = client.indicators.get_bbands(
                symbol,
                interval=interval,
                time_period=time_period,
                series_type=series_type,
                output_format=output_format
            )
        else:
            # Use generic indicator method
            data = client.indicators.get_indicator(
                indicator,
                symbol,
                interval=interval,
                time_period=time_period,
                series_type=series_type,
                output_format=output_format
            )
        
        if output_format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            click.echo(data)
            
    except AlphaVantageError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("from_currency")
@click.argument("to_currency")
@click.option(
    "--output-format",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Output format"
)
@click.option(
    "--daily/--rate",
    default=False,
    help="Get daily time series instead of exchange rate"
)
@click.pass_context
def get_forex(
    ctx,
    from_currency: str,
    to_currency: str,
    output_format: str,
    daily: bool
):
    """Get forex exchange rates or time series data."""
    client = get_client(ctx)
    try:
        if daily:
            data = client.forex.get_daily(
                from_currency,
                to_currency,
                output_format=output_format
            )
        else:
            data = client.forex.get_exchange_rate(
                from_currency,
                to_currency,
                output_format=output_format
            )
        
        if output_format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            click.echo(data)
            
    except AlphaVantageError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("symbol")
@click.argument("market", default="USD")
@click.option(
    "--output-format",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Output format"
)
@click.option(
    "--daily/--rate",
    default=False,
    help="Get daily time series instead of exchange rate"
)
@click.pass_context
def get_crypto(
    ctx,
    symbol: str,
    market: str,
    output_format: str,
    daily: bool
):
    """Get cryptocurrency data."""
    client = get_client(ctx)
    try:
        if daily:
            data = client.crypto.get_daily(
                symbol,
                market,
                output_format=output_format
            )
        else:
            data = client.crypto.get_exchange_rate(
                symbol,
                market,
                output_format=output_format
            )
        
        if output_format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            click.echo(data)
            
    except AlphaVantageError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def list_indicators(ctx):
    """List available technical indicators."""
    client = get_client(ctx)
    indicators = client.indicators.list_indicators()
    
    click.echo("Available Technical Indicators:")
    click.echo("=" * 50)
    
    for code, description in sorted(indicators.items()):
        click.echo(f"{code:12} - {description}")


@cli.command()
@click.argument("symbol")
@click.option(
    "--output-format",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Output format"
)
@click.pass_context
def get_overview(ctx, symbol: str, output_format: str):
    """Get company overview and fundamental data."""
    client = get_client(ctx)
    try:
        data = client.stocks.get_overview(symbol, output_format)
        
        if output_format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            click.echo(data)
            
    except AlphaVantageError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """Show version information."""
    from . import __version__, __description__
    click.echo(f"Alpha Vantage CLI v{__version__}")
    click.echo(__description__)


if __name__ == "__main__":
    cli()
