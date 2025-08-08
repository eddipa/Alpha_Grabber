"""Cryptocurrency data endpoints."""

from typing import Dict, Any, Optional
import pandas as pd

from ..exceptions import AlphaVantageError
from ..utils import format_output


class CryptoEndpoint:
    """Handler for cryptocurrency data endpoints."""
    
    def __init__(self, client):
        """Initialize with client reference."""
        self.client = client
    
    def get_exchange_rate(
        self,
        from_currency: str,
        to_currency: str,
        output_format: str = "json"
    ) -> Any:
        """
        Get real-time exchange rate for cryptocurrency.
        
        Args:
            from_currency: Cryptocurrency code (e.g., 'BTC')
            to_currency: Target currency code (e.g., 'USD')
            output_format: Output format ('json' or 'csv')
            
        Returns:
            Exchange rate data in requested format
        """
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": from_currency.upper(),
            "to_currency": to_currency.upper()
        }
        
        data = self.client._make_request(params)
        
        # Extract exchange rate data
        if "Realtime Currency Exchange Rate" not in data:
            raise AlphaVantageError("No exchange rate data found in response")
        
        rate_data = data["Realtime Currency Exchange Rate"]
        
        return format_output(rate_data, output_format)
    
    def get_intraday(
        self,
        symbol: str,
        market: str = "USD",
        interval: str = "5min",
        output_format: str = "json",
        outputsize: str = "compact"
    ) -> Any:
        """
        Get intraday cryptocurrency time series data.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC')
            market: Market currency (e.g., 'USD')
            interval: Time interval ('1min', '5min', '15min', '30min', '60min')
            output_format: Output format ('json' or 'csv')
            outputsize: 'compact' (latest 100 data points) or 'full'
            
        Returns:
            Intraday crypto data in requested format
        """
        params = {
            "function": "CRYPTO_INTRADAY",
            "symbol": symbol.upper(),
            "market": market.upper(),
            "interval": interval,
            "outputsize": outputsize
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series (Crypto)" in key or "Time Series Crypto" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No crypto time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
    
    def get_daily(
        self,
        symbol: str,
        market: str = "USD",
        output_format: str = "json"
    ) -> Any:
        """
        Get daily cryptocurrency time series data.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC')
            market: Market currency (e.g., 'USD')
            output_format: Output format ('json' or 'csv')
            
        Returns:
            Daily crypto data in requested format
        """
        params = {
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": symbol.upper(),
            "market": market.upper()
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series (Digital Currency Daily)" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No crypto time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
    
    def get_weekly(
        self,
        symbol: str,
        market: str = "USD",
        output_format: str = "json"
    ) -> Any:
        """
        Get weekly cryptocurrency time series data.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC')
            market: Market currency (e.g., 'USD')
            output_format: Output format ('json' or 'csv')
            
        Returns:
            Weekly crypto data in requested format
        """
        params = {
            "function": "DIGITAL_CURRENCY_WEEKLY",
            "symbol": symbol.upper(),
            "market": market.upper()
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series (Digital Currency Weekly)" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No crypto time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
    
    def get_monthly(
        self,
        symbol: str,
        market: str = "USD",
        output_format: str = "json"
    ) -> Any:
        """
        Get monthly cryptocurrency time series data.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC')
            market: Market currency (e.g., 'USD')
            output_format: Output format ('json' or 'csv')
            
        Returns:
            Monthly crypto data in requested format
        """
        params = {
            "function": "DIGITAL_CURRENCY_MONTHLY",
            "symbol": symbol.upper(),
            "market": market.upper()
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series (Digital Currency Monthly)" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No crypto time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
