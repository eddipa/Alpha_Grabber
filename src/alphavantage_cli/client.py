"""Main client class for Alpha Vantage API."""

import os
import time
from typing import Optional, Dict, Any
import requests

from .config import Config
from .exceptions import (
    AlphaVantageError,
    APIKeyError,
    RateLimitError,
    InvalidSymbolError,
    NetworkError,
)
from .endpoints.stocks import StocksEndpoint
from .endpoints.forex import ForexEndpoint
from .endpoints.crypto import CryptoEndpoint
from .endpoints.indicators import IndicatorsEndpoint


class AlphaVantageClient:
    """Main client for interacting with the Alpha Vantage API."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        rate_limit_delay: Optional[float] = None,
        config_file: Optional[str] = None,
    ):
        """
        Initialize the Alpha Vantage client.
        
        Args:
            api_key: Alpha Vantage API key. If not provided, will look for
                    ALPHA_VANTAGE_API_KEY environment variable or config file.
            base_url: Base URL for Alpha Vantage API. Defaults to official URL.
            rate_limit_delay: Delay between requests in seconds. Defaults to 12s for free tier.
            config_file: Path to configuration file.
        """
        self.config = Config(config_file)
        
        # Set API key with precedence: parameter > env var > config file
        self.api_key = (
            api_key or 
            os.getenv("ALPHA_VANTAGE_API_KEY") or 
            self.config.get("api_key")
        )
        
        if not self.api_key:
            raise APIKeyError(
                "Alpha Vantage API key is required. Set ALPHA_VANTAGE_API_KEY "
                "environment variable, provide api_key parameter, or add to config file."
            )
        
        # Set base URL
        self.base_url = (
            base_url or
            os.getenv("ALPHA_VANTAGE_BASE_URL") or
            self.config.get("base_url", "https://www.alphavantage.co/query")
        )
        
        # Set rate limiting
        self.rate_limit_delay = (
            rate_limit_delay or
            float(self.config.get("rate_limit_delay", 12.0))
        )
        self._last_request_time = 0.0
        
        # Initialize session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "alphavantage-cli/1.0.0",
            "Accept": "application/json",
        })
        
        # Initialize endpoint handlers
        self.stocks = StocksEndpoint(self)
        self.forex = ForexEndpoint(self)
        self.crypto = CryptoEndpoint(self)
        self.indicators = IndicatorsEndpoint(self)
    
    def _rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            time.sleep(sleep_time)
        
        self._last_request_time = time.time()
    
    def _make_request(
        self, 
        params: Dict[str, Any], 
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """
        Make a request to the Alpha Vantage API.
        
        Args:
            params: Query parameters for the API request
            timeout: Request timeout in seconds
            
        Returns:
            JSON response from the API
            
        Raises:
            APIKeyError: If API key is invalid
            RateLimitError: If rate limit is exceeded
            InvalidSymbolError: If symbol is invalid
            NetworkError: If network request fails
            AlphaVantageError: For other API errors
        """
        # Enforce rate limiting
        self._rate_limit()
        
        # Add API key to parameters
        params = params.copy()
        params["apikey"] = self.api_key
        
        try:
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=timeout
            )
            response.raise_for_status()
            
            # Parse JSON response
            try:
                data = response.json()
            except ValueError as e:
                raise AlphaVantageError(f"Invalid JSON response: {e}")
            
            # Check for API errors
            self._check_api_errors(data)
            
            return data
            
        except requests.exceptions.Timeout:
            raise NetworkError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Connection error")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise APIKeyError("Invalid API key")
            elif e.response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            else:
                raise NetworkError(f"HTTP error {e.response.status_code}: {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed: {e}")
    
    def _check_api_errors(self, data: Dict[str, Any]) -> None:
        """
        Check API response for errors.
        
        Args:
            data: JSON response from API
            
        Raises:
            APIKeyError: If API key is invalid
            RateLimitError: If rate limit exceeded
            InvalidSymbolError: If symbol is invalid
            AlphaVantageError: For other API errors
        """
        # Check for error message
        if "Error Message" in data:
            error_msg = data["Error Message"]
            if "Invalid API call" in error_msg:
                raise InvalidSymbolError(error_msg)
            else:
                raise AlphaVantageError(error_msg)
        
        # Check for information/note about API key
        if "Information" in data:
            info_msg = data["Information"]
            if "API key" in info_msg:
                raise APIKeyError(info_msg)
            elif "premium" in info_msg.lower() or "subscription" in info_msg.lower():
                raise AlphaVantageError(f"Premium feature required: {info_msg}")
            else:
                raise AlphaVantageError(info_msg)
        
        # Check for rate limiting note
        if "Note" in data:
            note_msg = data["Note"]
            if "rate limit" in note_msg.lower() or "frequent" in note_msg.lower():
                raise RateLimitError(note_msg)
            else:
                raise AlphaVantageError(note_msg)
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def close(self) -> None:
        """Close the HTTP session."""
        if hasattr(self, 'session'):
            self.session.close()
