"""Foreign exchange data endpoints."""

from typing import Dict, Any, Optional
import pandas as pd

from ..exceptions import AlphaVantageError
from ..utils import format_output


class ForexEndpoint:
    """Handler for foreign exchange data endpoints."""
    
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
        Get real-time exchange rate between two currencies.
        
        Args:
            from_currency: Source currency code (e.g., 'USD')
            to_currency: Target currency code (e.g., 'EUR')
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
        from_symbol: str,
        to_symbol: str,
        interval: str = "5min",
        output_format: str = "json",
        outputsize: str = "compact"
    ) -> Any:
        """
        Get intraday forex time series data.
        
        Args:
            from_symbol: Source currency code
            to_symbol: Target currency code
            interval: Time interval ('1min', '5min', '15min', '30min', '60min')
            output_format: Output format ('json' or 'csv')
            outputsize: 'compact' (latest 100 data points) or 'full'
            
        Returns:
            Intraday forex data in requested format
        """
        params = {
            "function": "FX_INTRADAY",
            "from_symbol": from_symbol.upper(),
            "to_symbol": to_symbol.upper(),
            "interval": interval,
            "outputsize": outputsize
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series FX" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No forex time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
    
    def get_daily(
        self,
        from_symbol: str,
        to_symbol: str,
        output_format: str = "json",
        outputsize: str = "compact"
    ) -> Any:
        """
        Get daily forex time series data.
        
        Args:
            from_symbol: Source currency code
            to_symbol: Target currency code
            output_format: Output format ('json' or 'csv')
            outputsize: 'compact' (latest 100 data points) or 'full'
            
        Returns:
            Daily forex data in requested format
        """
        params = {
            "function": "FX_DAILY",
            "from_symbol": from_symbol.upper(),
            "to_symbol": to_symbol.upper(),
            "outputsize": outputsize
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series FX" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No forex time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
    
    def get_weekly(
        self,
        from_symbol: str,
        to_symbol: str,
        output_format: str = "json"
    ) -> Any:
        """
        Get weekly forex time series data.
        
        Args:
            from_symbol: Source currency code
            to_symbol: Target currency code
            output_format: Output format ('json' or 'csv')
            
        Returns:
            Weekly forex data in requested format
        """
        params = {
            "function": "FX_WEEKLY",
            "from_symbol": from_symbol.upper(),
            "to_symbol": to_symbol.upper()
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series FX" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No forex time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
    
    def get_monthly(
        self,
        from_symbol: str,
        to_symbol: str,
        output_format: str = "json"
    ) -> Any:
        """
        Get monthly forex time series data.
        
        Args:
            from_symbol: Source currency code
            to_symbol: Target currency code
            output_format: Output format ('json' or 'csv')
            
        Returns:
            Monthly forex data in requested format
        """
        params = {
            "function": "FX_MONTHLY",
            "from_symbol": from_symbol.upper(),
            "to_symbol": to_symbol.upper()
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series FX" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No forex time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
