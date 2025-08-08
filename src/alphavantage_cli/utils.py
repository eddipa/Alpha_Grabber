"""Utility functions for Alpha Vantage CLI."""

import json
import io
from typing import Any, Dict, Union
import pandas as pd

from .exceptions import DataFormatError


def format_output(data: Dict[str, Any], output_format: str) -> Union[str, Dict[str, Any]]:
    """
    Format data for output in the requested format.
    
    Args:
        data: Data dictionary to format
        output_format: Output format ('json' or 'csv')
        
    Returns:
        Formatted data as string (CSV) or dict (JSON)
        
    Raises:
        DataFormatError: If formatting fails
    """
    if output_format.lower() == "json":
        return data
    elif output_format.lower() == "csv":
        return convert_to_csv(data)
    else:
        raise DataFormatError(f"Unsupported output format: {output_format}")


def convert_to_csv(data: Dict[str, Any]) -> str:
    """
    Convert JSON data to CSV format.
    
    Args:
        data: Data dictionary to convert
        
    Returns:
        CSV formatted string
        
    Raises:
        DataFormatError: If conversion fails
    """
    try:
        # Handle different data structures
        if not data:
            return ""
        
        # Check if data is a time series (nested dict with dates as keys)
        if is_time_series_data(data):
            return time_series_to_csv(data)
        
        # Handle flat dictionary (like quote data)
        elif is_flat_dict(data):
            return flat_dict_to_csv(data)
        
        # Handle other structures - convert to DataFrame
        else:
            df = pd.DataFrame([data])
            return df.to_csv(index=False)
            
    except Exception as e:
        raise DataFormatError(f"Failed to convert data to CSV: {e}")


def is_time_series_data(data: Dict[str, Any]) -> bool:
    """
    Check if data appears to be time series data.
    
    Args:
        data: Data dictionary to check
        
    Returns:
        True if data appears to be time series
    """
    if not isinstance(data, dict):
        return False
    
    # Check if all keys look like dates and values are dicts
    for key, value in data.items():
        if isinstance(value, dict):
            # Check if key looks like a date/timestamp
            if (
                "-" in key or 
                "/" in key or 
                ":" in key or
                len(key) >= 8  # Minimum date length
            ):
                continue
            else:
                return False
        else:
            return False
    
    return True


def is_flat_dict(data: Dict[str, Any]) -> bool:
    """
    Check if data is a flat dictionary (no nested dicts).
    
    Args:
        data: Data dictionary to check
        
    Returns:
        True if data is flat
    """
    if not isinstance(data, dict):
        return False
    
    for value in data.values():
        if isinstance(value, dict):
            return False
    
    return True


def time_series_to_csv(data: Dict[str, Any]) -> str:
    """
    Convert time series data to CSV format.
    
    Args:
        data: Time series data dictionary
        
    Returns:
        CSV formatted string
    """
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    
    # Reset index to make dates a column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'date'}, inplace=True)
    
    # Sort by date (most recent first)
    df.sort_values('date', ascending=False, inplace=True)
    
    return df.to_csv(index=False)


def flat_dict_to_csv(data: Dict[str, Any]) -> str:
    """
    Convert flat dictionary to CSV format.
    
    Args:
        data: Flat data dictionary
        
    Returns:
        CSV formatted string
    """
    # Create DataFrame with single row
    df = pd.DataFrame([data])
    return df.to_csv(index=False)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names for better CSV output.
    
    Args:
        df: DataFrame to clean
        
    Returns:
        DataFrame with cleaned column names
    """
    # Remove common prefixes from Alpha Vantage responses
    df.columns = df.columns.str.replace(r'^\d+\.\s*', '', regex=True)  # Remove "1. " prefix
    df.columns = df.columns.str.replace(r'\s+', '_', regex=True)  # Replace spaces with underscores
    df.columns = df.columns.str.lower()  # Convert to lowercase
    
    return df


def validate_symbol(symbol: str) -> str:
    """
    Validate and normalize a stock/currency symbol.
    
    Args:
        symbol: Symbol to validate
        
    Returns:
        Normalized symbol
        
    Raises:
        ValueError: If symbol is invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string")
    
    # Remove whitespace and convert to uppercase
    symbol = symbol.strip().upper()
    
    # Basic validation
    if not symbol.isalnum() and not all(c.isalnum() or c in '-.' for c in symbol):
        raise ValueError(f"Invalid symbol format: {symbol}")
    
    if len(symbol) > 10:
        raise ValueError(f"Symbol too long: {symbol}")
    
    return symbol


def validate_interval(interval: str) -> str:
    """
    Validate time interval parameter.
    
    Args:
        interval: Interval to validate
        
    Returns:
        Validated interval
        
    Raises:
        ValueError: If interval is invalid
    """
    valid_intervals = [
        "1min", "5min", "15min", "30min", "60min",
        "daily", "weekly", "monthly"
    ]
    
    if interval not in valid_intervals:
        raise ValueError(
            f"Invalid interval: {interval}. "
            f"Valid intervals: {', '.join(valid_intervals)}"
        )
    
    return interval


def format_currency_pair(from_currency: str, to_currency: str) -> tuple:
    """
    Format currency pair for API requests.
    
    Args:
        from_currency: Source currency
        to_currency: Target currency
        
    Returns:
        Tuple of (from_currency, to_currency) normalized
        
    Raises:
        ValueError: If currencies are invalid
    """
    if not from_currency or not to_currency:
        raise ValueError("Both currencies must be provided")
    
    from_currency = from_currency.strip().upper()
    to_currency = to_currency.strip().upper()
    
    # Basic validation
    if len(from_currency) < 2 or len(from_currency) > 5:
        raise ValueError(f"Invalid currency code: {from_currency}")
    
    if len(to_currency) < 2 or len(to_currency) > 5:
        raise ValueError(f"Invalid currency code: {to_currency}")
    
    return from_currency, to_currency


def format_error_message(error: Exception) -> str:
    """
    Format error message for user display.
    
    Args:
        error: Exception to format
        
    Returns:
        Formatted error message
    """
    error_msg = str(error)
    
    # Add helpful context for common errors
    if "API key" in error_msg.lower():
        error_msg += "\n\nTo get an API key, visit: https://www.alphavantage.co/support/#api-key"
    elif "rate limit" in error_msg.lower():
        error_msg += "\n\nConsider upgrading to a premium plan for higher rate limits."
    elif "invalid" in error_msg.lower() and "symbol" in error_msg.lower():
        error_msg += "\n\nPlease check that the symbol is correct and supported."
    
    return error_msg
