"""Alpha Grabber - Python package for Alpha Vantage financial market data API."""

from .client import AlphaVantageClient
from .exceptions import (
    AlphaVantageError,
    APIKeyError,
    RateLimitError,
    InvalidSymbolError,
    NetworkError,
)

__version__ = "1.0.0"
__author__ = "Alpha Grabber Team"
__email__ = "support@example.com"
__description__ = "Python package and CLI for Alpha Vantage financial market data API"

# Main exports
__all__ = [
    "AlphaVantageClient",
    "AlphaVantageError",
    "APIKeyError", 
    "RateLimitError",
    "InvalidSymbolError",
    "NetworkError",
]

# Package metadata
__package_name__ = "alpha-grabber"
__license__ = "MIT"
__url__ = "https://github.com/example/alpha-grabber"
