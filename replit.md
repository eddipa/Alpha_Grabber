# Alpha Vantage CLI

## Overview

A comprehensive Python package and command-line interface for accessing Alpha Vantage financial market data API. The system provides a modular architecture for retrieving stocks, forex, cryptocurrency, and technical indicators data with support for multiple output formats (JSON and CSV), configuration management, and built-in rate limiting.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Package Structure
- **Modular endpoint design**: Separate endpoint handlers for stocks, forex, cryptocurrency, and technical indicators
- **Client-based architecture**: Central `AlphaVantageClient` class that manages API connections and delegates to specialized endpoint handlers
- **Command-line interface**: Click-based CLI with group commands and options for easy terminal usage

### Core Components

#### Client Layer (`client.py`)
- Main `AlphaVantageClient` class serves as the primary interface
- Handles API key management with multiple sources (parameter, environment variable, config file)
- Implements rate limiting with configurable delays (default 12s for free tier)
- Manages HTTP requests and error handling
- Instantiates endpoint handlers (stocks, forex, crypto, indicators)

#### Endpoint Architecture (`endpoints/`)
- **Modular endpoint classes**: Each financial data type has its own handler class
- **Consistent interface**: All endpoints follow similar patterns for data retrieval
- **Format flexibility**: Support for both JSON and CSV output formats
- **Error handling**: Comprehensive validation and error reporting

#### Configuration Management (`config.py`)
- ConfigParser-based configuration system
- Support for external config files (INI format)
- Default configuration with overrides
- Environment variable integration

#### CLI Interface (`cli.py`)
- Click framework for command-line interface
- Group-based command structure for different data types
- Context passing for client configuration
- Consistent error handling and user feedback

#### Error Handling (`exceptions.py`)
- Custom exception hierarchy for different error types
- Specific exceptions for API keys, rate limits, invalid symbols, and network issues
- Comprehensive error messages for better user experience

#### Utilities (`utils.py`)
- Data formatting functions for output conversion
- JSON to CSV transformation capabilities
- Pandas integration for data manipulation

### Data Flow Architecture
1. CLI commands parse user input and options
2. Client initialization with API key validation
3. Request routing to appropriate endpoint handler
4. API request construction and execution
5. Response validation and error checking
6. Data formatting based on output preference
7. Result presentation to user

### Testing Strategy
- Comprehensive test coverage for all major components
- Mock-based testing for external API interactions
- Separate test files for CLI, client, and endpoint functionality
- Click's testing utilities for CLI command testing

## External Dependencies

### Core Dependencies
- **requests (>=2.28.0)**: HTTP client for Alpha Vantage API communication
- **click (>=8.0.0)**: Command-line interface framework
- **pandas (>=1.5.0)**: Data manipulation and CSV output formatting
- **configparser (>=5.0.0)**: Configuration file management

### Development Dependencies
- **pytest (>=7.0.0)**: Testing framework
- **pytest-cov (>=4.0.0)**: Test coverage reporting
- **black (>=22.0.0)**: Code formatting
- **flake8 (>=5.0.0)**: Code linting
- **mypy (>=1.0.0)**: Static type checking

### External Services
- **Alpha Vantage API**: Primary data source for financial market information
  - Base URL: https://www.alphavantage.co/query
  - Requires API key authentication
  - Rate limited (12 seconds between requests for free tier)
  - Supports multiple data types: stocks, forex, crypto, technical indicators

### Package Distribution
- **PyPI**: Configured for distribution as `alphavantage-cli` package
- **setuptools**: Package building and distribution management
- **Console scripts**: Entry points for `alphavantage` and `av` commands