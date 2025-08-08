"""Stock market data endpoints."""

from typing import Dict, Any, Optional
import pandas as pd

from ..exceptions import AlphaVantageError
from ..utils import format_output


class StocksEndpoint:
    """Handler for stock market data endpoints."""
    
    def __init__(self, client):
        """Initialize with client reference."""
        self.client = client
    
    def get_quote(self, symbol: str, output_format: str = "json") -> Any:
        """
        Get real-time quote for a stock symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
            output_format: Output format ('json' or 'csv')
            
        Returns:
            Quote data in requested format
        """
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol.upper()
        }
        
        data = self.client._make_request(params)
        
        # Extract quote data
        if "Global Quote" not in data:
            raise AlphaVantageError("No quote data found in response")
        
        quote_data = data["Global Quote"]
        
        return format_output(quote_data, output_format)
    
    def get_intraday(
        self,
        symbol: str,
        interval: str = "5min",
        adjusted: bool = True,
        output_format: str = "json",
        outputsize: str = "compact"
    ) -> Any:
        """
        Get intraday time series data.
        
        Args:
            symbol: Stock symbol
            interval: Time interval ('1min', '5min', '15min', '30min', '60min')
            adjusted: Whether to return adjusted data
            output_format: Output format ('json' or 'csv')
            outputsize: 'compact' (latest 100 data points) or 'full'
            
        Returns:
            Intraday data in requested format
        """
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol.upper(),
            "interval": interval,
            "adjusted": "true" if adjusted else "false",
            "outputsize": outputsize
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
    
    def get_daily(
        self,
        symbol: str,
        adjusted: bool = True,
        output_format: str = "json",
        outputsize: str = "compact"
    ) -> Any:
        """
        Get daily time series data.
        
        Args:
            symbol: Stock symbol
            adjusted: Whether to return adjusted data
            output_format: Output format ('json' or 'csv')
            outputsize: 'compact' (latest 100 data points) or 'full'
            
        Returns:
            Daily data in requested format
        """
        function = "TIME_SERIES_DAILY_ADJUSTED" if adjusted else "TIME_SERIES_DAILY"
        
        params = {
            "function": function,
            "symbol": symbol.upper(),
            "outputsize": outputsize
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
    
    def get_weekly(
        self,
        symbol: str,
        adjusted: bool = True,
        output_format: str = "json"
    ) -> Any:
        """
        Get weekly time series data.
        
        Args:
            symbol: Stock symbol
            adjusted: Whether to return adjusted data
            output_format: Output format ('json' or 'csv')
            
        Returns:
            Weekly data in requested format
        """
        function = "TIME_SERIES_WEEKLY_ADJUSTED" if adjusted else "TIME_SERIES_WEEKLY"
        
        params = {
            "function": function,
            "symbol": symbol.upper()
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
    
    def get_monthly(
        self,
        symbol: str,
        adjusted: bool = True,
        output_format: str = "json"
    ) -> Any:
        """
        Get monthly time series data.
        
        Args:
            symbol: Stock symbol
            adjusted: Whether to return adjusted data
            output_format: Output format ('json' or 'csv')
            
        Returns:
            Monthly data in requested format
        """
        function = "TIME_SERIES_MONTHLY_ADJUSTED" if adjusted else "TIME_SERIES_MONTHLY"
        
        params = {
            "function": function,
            "symbol": symbol.upper()
        }
        
        data = self.client._make_request(params)
        
        # Find time series key
        time_series_key = None
        for key in data.keys():
            if "Time Series" in key:
                time_series_key = key
                break
        
        if not time_series_key:
            raise AlphaVantageError("No time series data found in response")
        
        time_series_data = data[time_series_key]
        
        return format_output(time_series_data, output_format)
    
    def get_overview(self, symbol: str, output_format: str = "json") -> Any:
        """
        Get company overview and fundamental data.
        
        Args:
            symbol: Stock symbol
            output_format: Output format ('json' or 'csv')
            
        Returns:
            Company overview data in requested format
        """
        params = {
            "function": "OVERVIEW",
            "symbol": symbol.upper()
        }
        
        data = self.client._make_request(params)
        
        # The overview data is returned directly
        if not data or "Symbol" not in data:
            raise AlphaVantageError("No overview data found in response")
        
        return format_output(data, output_format)
