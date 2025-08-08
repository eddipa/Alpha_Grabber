"""Tests for Alpha Vantage client."""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
import requests

from alpha_grabber.client import AlphaVantageClient
from alpha_grabber.exceptions import (
    APIKeyError,
    RateLimitError,
    InvalidSymbolError,
    NetworkError,
    AlphaVantageError
)


class TestAlphaVantageClient:
    """Test cases for AlphaVantageClient."""
    
    def test_init_with_api_key(self):
        """Test client initialization with API key."""
        client = AlphaVantageClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://www.alphavantage.co/query"
        assert client.rate_limit_delay == 12.0
    
    def test_init_without_api_key(self):
        """Test client initialization without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(APIKeyError):
                AlphaVantageClient()
    
    def test_init_with_env_var(self):
        """Test client initialization with environment variable."""
        with patch.dict(os.environ, {"ALPHA_VANTAGE_API_KEY": "env_key"}):
            client = AlphaVantageClient()
            assert client.api_key == "env_key"
    
    def test_init_with_custom_params(self):
        """Test client initialization with custom parameters."""
        client = AlphaVantageClient(
            api_key="test_key",
            base_url="https://custom.url",
            rate_limit_delay=5.0
        )
        assert client.api_key == "test_key"
        assert client.base_url == "https://custom.url"
        assert client.rate_limit_delay == 5.0
    
    @patch('time.sleep')
    @patch('time.time')
    def test_rate_limiting(self, mock_time, mock_sleep):
        """Test rate limiting functionality."""
        # First test - should sleep full delay time  
        mock_time.side_effect = [0.0, 10.0]  # start_time, end_time
        
        client = AlphaVantageClient(api_key="test_key", rate_limit_delay=10.0)
        client._last_request_time = 0.0
        
        client._rate_limit()
        mock_sleep.assert_called_with(10.0)
        
        # Second test - should sleep remaining time
        mock_time.reset_mock()
        mock_sleep.reset_mock()
        mock_time.side_effect = [3.0, 13.0]  # 3 seconds after last request
        
        client._last_request_time = 0.0  # Last request was at time 0
        client._rate_limit()
        mock_sleep.assert_called_with(7.0)  # Should sleep 10 - 3 = 7 seconds
    
    def test_make_request_success(self):
        """Test successful API request."""
        client = AlphaVantageClient(api_key="test_key")
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.session, 'get', return_value=mock_response):
            with patch.object(client, '_rate_limit'):
                result = client._make_request({"function": "TEST"})
                assert result == {"test": "data"}
    
    def test_make_request_with_api_error_message(self):
        """Test API request with error message in response."""
        client = AlphaVantageClient(api_key="test_key")
        
        mock_response = Mock()
        mock_response.json.return_value = {"Error Message": "Invalid API call"}
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.session, 'get', return_value=mock_response):
            with patch.object(client, '_rate_limit'):
                with pytest.raises(InvalidSymbolError):
                    client._make_request({"function": "TEST"})
    
    def test_make_request_with_rate_limit_note(self):
        """Test API request with rate limit note."""
        client = AlphaVantageClient(api_key="test_key")
        
        mock_response = Mock()
        mock_response.json.return_value = {"Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 25 requests per day."}
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.session, 'get', return_value=mock_response):
            with patch.object(client, '_rate_limit'):
                with pytest.raises(RateLimitError):
                    client._make_request({"function": "TEST"})
    
    def test_make_request_with_api_key_info(self):
        """Test API request with API key information."""
        client = AlphaVantageClient(api_key="test_key")
        
        mock_response = Mock()
        mock_response.json.return_value = {"Information": "Please visit https://www.alphavantage.co/support/#api-key to claim your free API key."}
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client.session, 'get', return_value=mock_response):
            with patch.object(client, '_rate_limit'):
                with pytest.raises(APIKeyError):
                    client._make_request({"function": "TEST"})
    
    def test_make_request_network_error(self):
        """Test API request with network error."""
        client = AlphaVantageClient(api_key="test_key")
        
        with patch.object(client.session, 'get', side_effect=requests.exceptions.ConnectionError("Connection failed")):
            with patch.object(client, '_rate_limit'):
                with pytest.raises(NetworkError):
                    client._make_request({"function": "TEST"})
    
    def test_make_request_timeout(self):
        """Test API request with timeout."""
        client = AlphaVantageClient(api_key="test_key")
        
        with patch.object(client.session, 'get', side_effect=requests.exceptions.Timeout("Request timed out")):
            with patch.object(client, '_rate_limit'):
                with pytest.raises(NetworkError):
                    client._make_request({"function": "TEST"})
    
    def test_make_request_http_error_401(self):
        """Test API request with 401 HTTP error."""
        client = AlphaVantageClient(api_key="test_key")
        
        mock_response = Mock()
        mock_response.status_code = 401
        http_error = requests.exceptions.HTTPError("401 Unauthorized")
        http_error.response = mock_response
        
        with patch.object(client.session, 'get', side_effect=http_error):
            with patch.object(client, '_rate_limit'):
                with pytest.raises(APIKeyError):
                    client._make_request({"function": "TEST"})
    
    def test_make_request_http_error_429(self):
        """Test API request with 429 HTTP error."""
        client = AlphaVantageClient(api_key="test_key")
        
        mock_response = Mock()
        mock_response.status_code = 429
        http_error = requests.exceptions.HTTPError("429 Too Many Requests")
        http_error.response = mock_response
        
        with patch.object(client.session, 'get', side_effect=http_error):
            with patch.object(client, '_rate_limit'):
                with pytest.raises(RateLimitError):
                    client._make_request({"function": "TEST"})
    
    def test_context_manager(self):
        """Test client as context manager."""
        with AlphaVantageClient(api_key="test_key") as client:
            assert isinstance(client, AlphaVantageClient)
            assert client.api_key == "test_key"
    
    def test_close(self):
        """Test client close method."""
        client = AlphaVantageClient(api_key="test_key")
        mock_session = Mock()
        client.session = mock_session
        
        client.close()
        mock_session.close.assert_called_once()
