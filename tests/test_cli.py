"""Tests for CLI functionality."""

import pytest
import json
from unittest.mock import Mock, patch
from click.testing import CliRunner

from alphavantage_cli.cli import cli
from alphavantage_cli.exceptions import APIKeyError, AlphaVantageError


class TestCLI:
    """Test cases for CLI commands."""
    
    def setup_method(self):
        """Setup test runner."""
        self.runner = CliRunner()
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_get_quote_success(self, mock_client_class):
        """Test successful quote command."""
        mock_client = Mock()
        mock_client.stocks.get_quote.return_value = {
            "01. symbol": "AAPL",
            "05. price": "150.00"
        }
        mock_client_class.return_value = mock_client
        
        result = self.runner.invoke(cli, [
            '--api-key', 'test_key',
            'get-quote', 'AAPL'
        ])
        
        assert result.exit_code == 0
        assert "AAPL" in result.output
        assert "150.00" in result.output
        mock_client.stocks.get_quote.assert_called_once_with('AAPL', 'json')
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_get_quote_csv_format(self, mock_client_class):
        """Test quote command with CSV output."""
        mock_client = Mock()
        mock_client.stocks.get_quote.return_value = "symbol,price\nAAPL,150.00"
        mock_client_class.return_value = mock_client
        
        result = self.runner.invoke(cli, [
            '--api-key', 'test_key',
            'get-quote', 'AAPL',
            '--output-format', 'csv'
        ])
        
        assert result.exit_code == 0
        assert "symbol,price" in result.output
        mock_client.stocks.get_quote.assert_called_once_with('AAPL', 'csv')
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_get_daily_success(self, mock_client_class):
        """Test successful daily command."""
        mock_client = Mock()
        mock_client.stocks.get_daily.return_value = {
            "2023-01-01": {"1. open": "150.00", "4. close": "155.00"}
        }
        mock_client_class.return_value = mock_client
        
        result = self.runner.invoke(cli, [
            '--api-key', 'test_key',
            'get-daily', 'AAPL',
            '--adjusted'
        ])
        
        assert result.exit_code == 0
        mock_client.stocks.get_daily.assert_called_once_with(
            'AAPL',
            adjusted=True,
            output_format='json',
            outputsize='compact'
        )
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_get_indicators_sma(self, mock_client_class):
        """Test indicators command with SMA."""
        mock_client = Mock()
        mock_client.indicators.get_sma.return_value = {
            "2023-01-01": {"SMA": "150.00"}
        }
        mock_client_class.return_value = mock_client
        
        result = self.runner.invoke(cli, [
            '--api-key', 'test_key',
            'get-indicators', 'AAPL',
            '--indicator', 'SMA',
            '--time-period', '20'
        ])
        
        assert result.exit_code == 0
        mock_client.indicators.get_sma.assert_called_once_with(
            'AAPL',
            interval='daily',
            time_period=20,
            series_type='close',
            output_format='json'
        )
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_get_indicators_generic(self, mock_client_class):
        """Test indicators command with generic indicator."""
        mock_client = Mock()
        mock_client.indicators.get_indicator.return_value = {
            "2023-01-01": {"CUSTOM": "100.00"}
        }
        mock_client_class.return_value = mock_client
        
        result = self.runner.invoke(cli, [
            '--api-key', 'test_key',
            'get-indicators', 'AAPL',
            '--indicator', 'CUSTOM',
            '--time-period', '14'
        ])
        
        assert result.exit_code == 0
        mock_client.indicators.get_indicator.assert_called_once_with(
            'CUSTOM',
            'AAPL',
            interval='daily',
            time_period=14,
            series_type='close',
            output_format='json'
        )
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_get_forex_rate(self, mock_client_class):
        """Test forex command for exchange rate."""
        mock_client = Mock()
        mock_client.forex.get_exchange_rate.return_value = {
            "1. From_Currency Code": "USD",
            "3. To_Currency Code": "EUR",
            "5. Exchange Rate": "0.85"
        }
        mock_client_class.return_value = mock_client
        
        result = self.runner.invoke(cli, [
            '--api-key', 'test_key',
            'get-forex', 'USD', 'EUR'
        ])
        
        assert result.exit_code == 0
        mock_client.forex.get_exchange_rate.assert_called_once_with(
            'USD', 'EUR', output_format='json'
        )
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_get_forex_daily(self, mock_client_class):
        """Test forex command for daily data."""
        mock_client = Mock()
        mock_client.forex.get_daily.return_value = {
            "2023-01-01": {"1. open": "0.85", "4. close": "0.86"}
        }
        mock_client_class.return_value = mock_client
        
        result = self.runner.invoke(cli, [
            '--api-key', 'test_key',
            'get-forex', 'USD', 'EUR',
            '--daily'
        ])
        
        assert result.exit_code == 0
        mock_client.forex.get_daily.assert_called_once_with(
            'USD', 'EUR', output_format='json'
        )
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_get_crypto_rate(self, mock_client_class):
        """Test crypto command for exchange rate."""
        mock_client = Mock()
        mock_client.crypto.get_exchange_rate.return_value = {
            "1. From_Currency Code": "BTC",
            "3. To_Currency Code": "USD",
            "5. Exchange Rate": "45000.00"
        }
        mock_client_class.return_value = mock_client
        
        result = self.runner.invoke(cli, [
            '--api-key', 'test_key',
            'get-crypto', 'BTC'
        ])
        
        assert result.exit_code == 0
        mock_client.crypto.get_exchange_rate.assert_called_once_with(
            'BTC', 'USD', output_format='json'
        )
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_list_indicators(self, mock_client_class):
        """Test list indicators command."""
        mock_client = Mock()
        mock_client.indicators.list_indicators.return_value = {
            "SMA": "Simple Moving Average",
            "EMA": "Exponential Moving Average"
        }
        mock_client_class.return_value = mock_client
        
        result = self.runner.invoke(cli, [
            '--api-key', 'test_key',
            'list-indicators'
        ])
        
        assert result.exit_code == 0
        assert "SMA" in result.output
        assert "Simple Moving Average" in result.output
        assert "EMA" in result.output
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_version_command(self, mock_client_class):
        """Test version command."""
        mock_client_class.return_value = Mock()
        
        result = self.runner.invoke(cli, [
            '--api-key', 'test_key',
            'version'
        ])
        
        assert result.exit_code == 0
        assert "Alpha Vantage CLI" in result.output
        assert "v1.0.0" in result.output
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_api_key_error(self, mock_client_class):
        """Test CLI with API key error."""
        mock_client_class.side_effect = APIKeyError("Invalid API key")
        
        result = self.runner.invoke(cli, [
            'get-quote', 'AAPL'
        ])
        
        assert result.exit_code == 1
        assert "Invalid API key" in result.output
        assert "alphavantage.co" in result.output
    
    @patch('alphavantage_cli.cli.AlphaVantageClient')
    def test_alpha_vantage_error_in_command(self, mock_client_class):
        """Test Alpha Vantage error during command execution."""
        mock_client = Mock()
        mock_client.stocks.get_quote.side_effect = AlphaVantageError("API error")
        mock_client_class.return_value = mock_client
        
        result = self.runner.invoke(cli, [
            '--api-key', 'test_key',
            'get-quote', 'INVALID'
        ])
        
        assert result.exit_code == 1
        assert "API error" in result.output
    
    def test_cli_help(self):
        """Test CLI help output."""
        result = self.runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert "Alpha Vantage CLI" in result.output
        assert "get-quote" in result.output
        assert "get-daily" in result.output
        assert "get-indicators" in result.output
    
    def test_command_help(self):
        """Test individual command help."""
        result = self.runner.invoke(cli, ['get-quote', '--help'])
        
        assert result.exit_code == 0
        assert "Get real-time stock quote" in result.output
        assert "--output-format" in result.output
