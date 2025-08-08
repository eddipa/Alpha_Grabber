"""Custom exceptions for Alpha Vantage CLI."""


class AlphaVantageError(Exception):
    """Base exception for Alpha Vantage API errors."""
    pass


class APIKeyError(AlphaVantageError):
    """Exception raised for API key related errors."""
    pass


class RateLimitError(AlphaVantageError):
    """Exception raised when API rate limit is exceeded."""
    pass


class InvalidSymbolError(AlphaVantageError):
    """Exception raised for invalid stock/currency symbols."""
    pass


class NetworkError(AlphaVantageError):
    """Exception raised for network-related errors."""
    pass


class ConfigurationError(AlphaVantageError):
    """Exception raised for configuration-related errors."""
    pass


class DataFormatError(AlphaVantageError):
    """Exception raised for data formatting errors."""
    pass
