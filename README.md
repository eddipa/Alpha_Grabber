# Alpha Grabber

A comprehensive Python package and command-line interface for accessing Alpha Vantage financial market data API.

## Features

- **Comprehensive API Coverage**: Access to stocks, forex, cryptocurrency, and technical indicators
- **Command-Line Interface**: Easy-to-use CLI for common operations
- **Multiple Output Formats**: Support for JSON and CSV output
- **Configuration Management**: API key and settings management
- **Rate Limiting**: Built-in handling of API rate limits
- **Error Handling**: Comprehensive error handling and validation
- **Pip Installable**: Proper Python package structure

## Installation

Install from PyPI (when published):

```bash
pip install alpha-grabber
```

Or install from source:

```bash
git clone <repository-url>
cd alpha-grabber
pip install -e .
```

## Configuration

You'll need an Alpha Vantage API key to use this tool. Get one free at https://www.alphavantage.co/support/#api-key

Set your API key using one of these methods:

1. **Environment variable** (recommended):
   ```bash
   export ALPHA_VANTAGE_API_KEY="your-api-key-here"
   ```

2. **Command line option**:
   ```bash
   alpha-grabber --api-key YOUR_API_KEY get-quote AAPL
   ```

3. **Configuration file**:
   Create a `config.ini` file:
   ```ini
   [DEFAULT]
   api_key = your-api-key-here
   rate_limit_delay = 12.0
   ```

## Usage

### Basic Help

```bash
# Show all available commands
alpha-grabber --help

# Show help for a specific command
alpha-grabber get-quote --help
```

### Stock Data

```bash
# Get real-time stock quote
alpha-grabber get-quote AAPL

# Get stock quote in CSV format
alpha-grabber get-quote AAPL --output-format csv

# Get daily stock data (last 100 days)
alpha-grabber get-daily AAPL

# Get full historical daily data
alpha-grabber get-daily AAPL --outputsize full

# Get intraday data (5-minute intervals)
alpha-grabber get-intraday AAPL --interval 5min

# Get company overview/fundamentals
alpha-grabber get-overview AAPL
```

### Technical Indicators

```bash
# List all available indicators
alpha-grabber list-indicators

# Get Simple Moving Average (20-period)
alpha-grabber get-indicators AAPL --indicator SMA --time-period 20

# Get RSI indicator
alpha-grabber get-indicators AAPL --indicator RSI --time-period 14

# Get MACD indicator
alpha-grabber get-indicators AAPL --indicator MACD

# Get Bollinger Bands
alpha-grabber get-indicators AAPL --indicator BBANDS --time-period 20
```

### Forex Data

```bash
# Get current exchange rate
alpha-grabber get-forex USD EUR

# Get forex daily time series
alpha-grabber get-forex USD EUR --daily

# Get forex data in CSV format
alpha-grabber get-forex USD EUR --output-format csv
```

### Cryptocurrency Data

```bash
# Get current crypto price (defaults to USD)
alpha-grabber get-crypto BTC

# Get crypto price in specific market
alpha-grabber get-crypto BTC EUR

# Get crypto daily time series
alpha-grabber get-crypto BTC --daily
```

### Advanced Usage

```bash
# Use custom rate limiting (faster than default 12s)
alpha-grabber --rate-limit 5.0 get-quote AAPL

# Use configuration file
alpha-grabber --config-file /path/to/config.ini get-quote AAPL

# Use shorthand command (av instead of alpha-grabber)
av get-quote AAPL
```

## Output Formats

All commands support two output formats:

- **JSON** (default): Pretty-printed JSON for easy reading
- **CSV**: Comma-separated values for spreadsheet import

Example JSON output:
```json
{
  "01. symbol": "AAPL",
  "05. price": "150.00",
  "07. latest trading day": "2023-12-01",
  "09. change": "+2.50",
  "10. change percent": "+1.69%"
}
```

## Error Handling

The tool provides helpful error messages for common issues:

- **Missing API key**: Clear instructions on how to set up your API key
- **Invalid symbols**: Suggestions for correct symbol format
- **Rate limiting**: Automatic handling with configurable delays
- **Network issues**: Retry suggestions and connectivity troubleshooting

## Rate Limiting

Alpha Vantage has rate limits:
- **Free tier**: 25 requests per day, 5 requests per minute
- **Paid tier**: Higher limits based on subscription

The tool automatically handles rate limiting with a default 12-second delay between requests (suitable for free tier). You can adjust this with `--rate-limit` option.

## Available Commands

| Command | Description |
|---------|-------------|
| `get-quote` | Get real-time stock quote |
| `get-daily` | Get daily time series data |
| `get-intraday` | Get intraday time series data |
| `get-overview` | Get company overview/fundamentals |
| `get-indicators` | Get technical indicators |
| `get-forex` | Get forex exchange rates or time series |
| `get-crypto` | Get cryptocurrency data |
| `list-indicators` | List all available technical indicators |
| `version` | Show version information |
