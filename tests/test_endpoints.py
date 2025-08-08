"""Tests for Alpha Vantage API endpoints."""

import pytest
from unittest.mock import Mock, patch

from alpha_grabber.client import AlphaVantageClient
from alpha_grabber.endpoints.stocks import StocksEndpoint
from alpha_grabber.endpoints.forex import ForexEndpoint
from alpha_grabber.endpoints.crypto import CryptoEndpoint
from alpha_grabber.endpoints.indicators import IndicatorsEndpoint
from alpha_grabber.exceptions import AlphaVantageError


class TestStocksEndpoint:
    """Test cases for StocksEndpoint."""
    
    def setup_method(self):
        """Setup test client and endpoint."""
        self.client = Mock(spec=AlphaVantageClient)
        self.endpoint = StocksEndpoint(self.client)
    
    def test_get_quote_success(self):
        """Test successful quote retrieval."""
        mock_data = {
            "Global Quote": {
                "01. symbol": "AAPL",
                "05. price": "150.00"
            }
        }
        self.client._make_request.return_value = mock_data
        
        with patch('alpha_grabber.endpoints.stocks.format_output') as mock_format:
            mock_format.return_value = mock_data["Global Quote"]
            
            result = self.endpoint.get_quote("AAPL")
            
            self.client._make_request.assert_called_once_with({
                "function": "GLOBAL_QUOTE",
                "symbol": "AAPL"
            })
            mock_format.assert_called_once_with(mock_data["Global Quote"], "json")
    
    def test_get_quote_no_data(self):
        """Test quote retrieval with no data."""
        mock_data = {"Meta Data": {"1. Information": "Daily Prices"}}
        self.client._make_request.return_value = mock_data
        
        with pytest.raises(AlphaVantageError, match="No quote data found"):
            self.endpoint.get_quote("INVALID")
    
    def test_get_daily_success(self):
        """Test successful daily data retrieval."""
        mock_data = {
            "Time Series (Daily)": {
                "2023-01-01": {
                    "1. open": "150.00",
                    "4. close": "155.00"
                }
            }
        }
        self.client._make_request.return_value = mock_data
        
        with patch('alpha_grabber.endpoints.stocks.format_output') as mock_format:
            mock_format.return_value = mock_data["Time Series (Daily)"]
            
            result = self.endpoint.get_daily("AAPL")
            
            self.client._make_request.assert_called_once_with({
                "function": "TIME_SERIES_DAILY_ADJUSTED",
                "symbol": "AAPL",
                "outputsize": "compact"
            })
    
    def test_get_daily_no_adjusted(self):
        """Test daily data retrieval without adjustment."""
        mock_data = {"Time Series (Daily)": {}}
        self.client._make_request.return_value = mock_data
        
        with patch('alpha_grabber.endpoints.stocks.format_output'):
            self.endpoint.get_daily("AAPL", adjusted=False)
            
            self.client._make_request.assert_called_once_with({
                "function": "TIME_SERIES_DAILY",
                "symbol": "AAPL",
                "outputsize": "compact"
            })
    
    def test_get_intraday_success(self):
        """Test successful intraday data retrieval."""
        mock_data = {
            "Time Series (5min)": {
                "2023-01-01 09:30:00": {
                    "1. open": "150.00",
                    "4. close": "155.00"
                }
            }
        }
        self.client._make_request.return_value = mock_data
        
        with patch('alpha_grabber.endpoints.stocks.format_output') as mock_format:
            mock_format.return_value = mock_data["Time Series (5min)"]
            
            result = self.endpoint.get_intraday("AAPL", interval="5min")
            
            self.client._make_request.assert_called_once_with({
                "function": "TIME_SERIES_INTRADAY",
                "symbol": "AAPL",
                "interval": "5min",
                "adjusted": "true",
                "outputsize": "compact"
            })


class TestForexEndpoint:
    """Test cases for ForexEndpoint."""
    
    def setup_method(self):
        """Setup test client and endpoint."""
        self.client = Mock(spec=AlphaVantageClient)
        self.endpoint = ForexEndpoint(self.client)
    
    def test_get_exchange_rate_success(self):
        """Test successful exchange rate retrieval."""
        mock_data = {
            "Realtime Currency Exchange Rate": {
                "1. From_Currency Code": "USD",
                "3. To_Currency Code": "EUR",
                "5. Exchange Rate": "0.85"
            }
        }
        self.client._make_request.return_value = mock_data
        
        with patch('alpha_grabber.endpoints.forex.format_output') as mock_format:
            mock_format.return_value = mock_data["Realtime Currency Exchange Rate"]
            
            result = self.endpoint.get_exchange_rate("USD", "EUR")
            
            self.client._make_request.assert_called_once_with({
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": "USD",
                "to_currency": "EUR"
            })
    
    def test_get_daily_success(self):
        """Test successful forex daily data retrieval."""
        mock_data = {
            "Time Series FX (Daily)": {
                "2023-01-01": {
                    "1. open": "0.85",
                    "4. close": "0.86"
                }
            }
        }
        self.client._make_request.return_value = mock_data
        
        with patch('alpha_grabber.endpoints.forex.format_output') as mock_format:
            mock_format.return_value = mock_data["Time Series FX (Daily)"]
            
            result = self.endpoint.get_daily("USD", "EUR")
            
            self.client._make_request.assert_called_once_with({
                "function": "FX_DAILY",
                "from_symbol": "USD",
                "to_symbol": "EUR",
                "outputsize": "compact"
            })


class TestCryptoEndpoint:
    """Test cases for CryptoEndpoint."""
    
    def setup_method(self):
        """Setup test client and endpoint."""
        self.client = Mock(spec=AlphaVantageClient)
        self.endpoint = CryptoEndpoint(self.client)
    
    def test_get_exchange_rate_success(self):
        """Test successful crypto exchange rate retrieval."""
        mock_data = {
            "Realtime Currency Exchange Rate": {
                "1. From_Currency Code": "BTC",
                "3. To_Currency Code": "USD",
                "5. Exchange Rate": "45000.00"
            }
        }
        self.client._make_request.return_value = mock_data
        
        with patch('alpha_grabber.endpoints.crypto.format_output') as mock_format:
            mock_format.return_value = mock_data["Realtime Currency Exchange Rate"]
            
            result = self.endpoint.get_exchange_rate("BTC", "USD")
            
            self.client._make_request.assert_called_once_with({
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": "BTC",
                "to_currency": "USD"
            })
    
    def test_get_daily_success(self):
        """Test successful crypto daily data retrieval."""
        mock_data = {
            "Time Series (Digital Currency Daily)": {
                "2023-01-01": {
                    "1a. open (USD)": "45000.00",
                    "4a. close (USD)": "46000.00"
                }
            }
        }
        self.client._make_request.return_value = mock_data
        
        with patch('alpha_grabber.endpoints.crypto.format_output') as mock_format:
            mock_format.return_value = mock_data["Time Series (Digital Currency Daily)"]
            
            result = self.endpoint.get_daily("BTC", "USD")
            
            self.client._make_request.assert_called_once_with({
                "function": "DIGITAL_CURRENCY_DAILY",
                "symbol": "BTC",
                "market": "USD"
            })


class TestIndicatorsEndpoint:
    """Test cases for IndicatorsEndpoint."""
    
    def setup_method(self):
        """Setup test client and endpoint."""
        self.client = Mock(spec=AlphaVantageClient)
        self.endpoint = IndicatorsEndpoint(self.client)
    
    def test_get_sma_success(self):
        """Test successful SMA retrieval."""
        mock_data = {
            "Technical Analysis: SMA": {
                "2023-01-01": {
                    "SMA": "150.00"
                }
            }
        }
        self.client._make_request.return_value = mock_data
        
        with patch('alpha_grabber.endpoints.indicators.format_output') as mock_format:
            mock_format.return_value = mock_data["Technical Analysis: SMA"]
            
            result = self.endpoint.get_sma("AAPL", time_period=20)
            
            self.client._make_request.assert_called_once_with({
                "function": "SMA",
                "symbol": "AAPL",
                "interval": "daily",
                "time_period": "20",
                "series_type": "close"
            })
    
    def test_get_indicator_unknown(self):
        """Test getting unknown indicator."""
        with pytest.raises(AlphaVantageError, match="Unknown indicator"):
            self.endpoint.get_indicator("UNKNOWN", "AAPL")
    
    def test_list_indicators(self):
        """Test listing available indicators."""
        indicators = self.endpoint.list_indicators()
        
        assert isinstance(indicators, dict)
        assert "SMA" in indicators
        assert "EMA" in indicators
        assert "RSI" in indicators
        assert "MACD" in indicators
        assert indicators["SMA"] == "Simple Moving Average"
    
    def test_get_indicator_with_params(self):
        """Test getting indicator with additional parameters."""
        mock_data = {
            "Technical Analysis: RSI": {
                "2023-01-01": {"RSI": "65.00"}
            }
        }
        self.client._make_request.return_value = mock_data
        
        with patch('alpha_grabber.endpoints.indicators.format_output') as mock_format:
            mock_format.return_value = mock_data["Technical Analysis: RSI"]
            
            result = self.endpoint.get_indicator(
                "RSI", 
                "AAPL", 
                time_period=14,
                series_type="close"
            )
            
            # Check that parameters were converted to strings
            call_args = self.client._make_request.call_args[0][0]
            assert call_args["time_period"] == "14"
            assert call_args["series_type"] == "close"
