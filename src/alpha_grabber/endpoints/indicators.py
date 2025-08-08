"""Technical indicators endpoints."""

from typing import Dict, Any, Optional
import pandas as pd

from ..exceptions import AlphaVantageError
from ..utils import format_output


class IndicatorsEndpoint:
    """Handler for technical indicators endpoints."""
    
    # Available technical indicators
    INDICATORS = {
        "SMA": "Simple Moving Average",
        "EMA": "Exponential Moving Average", 
        "WMA": "Weighted Moving Average",
        "DEMA": "Double Exponential Moving Average",
        "TEMA": "Triple Exponential Moving Average",
        "TRIMA": "Triangular Moving Average",
        "KAMA": "Kaufman Adaptive Moving Average",
        "MAMA": "MESA Adaptive Moving Average",
        "VWAP": "Volume Weighted Average Price",
        "T3": "Triple Exponential Moving Average (T3)",
        "MACD": "Moving Average Convergence/Divergence",
        "MACDEXT": "MACD with controllable MA type",
        "STOCH": "Stochastic",
        "STOCHF": "Stochastic Fast",
        "RSI": "Relative Strength Index",
        "STOCHRSI": "Stochastic Relative Strength Index",
        "WILLR": "Williams' %R",
        "ADX": "Average Directional Movement Index",
        "ADXR": "Average Directional Movement Index Rating",
        "APO": "Absolute Price Oscillator",
        "PPO": "Percentage Price Oscillator",
        "MOM": "Momentum",
        "BOP": "Balance Of Power",
        "CCI": "Commodity Channel Index",
        "CMO": "Chande Momentum Oscillator",
        "ROC": "Rate of change",
        "ROCR": "Rate of change ratio",
        "AROON": "Aroon",
        "AROONOSC": "Aroon Oscillator",
        "MFI": "Money Flow Index",
        "TRIX": "1-day Rate-Of-Change (ROC) of a Triple Smooth EMA",
        "ULTOSC": "Ultimate Oscillator",
        "DX": "Directional Movement Index",
        "MINUS_DI": "Minus Directional Indicator",
        "PLUS_DI": "Plus Directional Indicator",
        "MINUS_DM": "Minus Directional Movement",
        "PLUS_DM": "Plus Directional Movement",
        "BBANDS": "Bollinger Bands",
        "MIDPOINT": "MidPoint over period",
        "MIDPRICE": "Midpoint Price over period",
        "SAR": "Parabolic SAR",
        "TRANGE": "True Range",
        "ATR": "Average True Range",
        "NATR": "Normalized Average True Range",
        "CHAIKIN": "Chaikin A/D Line",
        "AD": "Chaikin A/D Line",
        "ADOSC": "Chaikin A/D Oscillator",
        "OBV": "On Balance Volume",
        "HT_TRENDLINE": "Hilbert Transform - Instantaneous Trendline",
        "HT_SINE": "Hilbert Transform - SineWave",
        "HT_TRENDMODE": "Hilbert Transform - Trend vs Cycle Mode",
        "HT_DCPERIOD": "Hilbert Transform - Dominant Cycle Period",
        "HT_DCPHASE": "Hilbert Transform - Dominant Cycle Phase",
        "HT_PHASOR": "Hilbert Transform - Phasor Components"
    }
    
    def __init__(self, client):
        """Initialize with client reference."""
        self.client = client
    
    def get_sma(
        self,
        symbol: str,
        interval: str = "daily",
        time_period: int = 20,
        series_type: str = "close",
        output_format: str = "json"
    ) -> Any:
        """
        Get Simple Moving Average (SMA).
        
        Args:
            symbol: Stock symbol
            interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly')
            time_period: Number of data points used to calculate the SMA
            series_type: Price type ('close', 'open', 'high', 'low')
            output_format: Output format ('json' or 'csv')
            
        Returns:
            SMA data in requested format
        """
        params = {
            "function": "SMA",
            "symbol": symbol.upper(),
            "interval": interval,
            "time_period": str(time_period),
            "series_type": series_type
        }
        
        data = self.client._make_request(params)
        
        # Find technical analysis key
        tech_key = None
        for key in data.keys():
            if "Technical Analysis" in key:
                tech_key = key
                break
        
        if not tech_key:
            raise AlphaVantageError("No technical analysis data found in response")
        
        tech_data = data[tech_key]
        
        return format_output(tech_data, output_format)
    
    def get_ema(
        self,
        symbol: str,
        interval: str = "daily",
        time_period: int = 20,
        series_type: str = "close",
        output_format: str = "json"
    ) -> Any:
        """
        Get Exponential Moving Average (EMA).
        
        Args:
            symbol: Stock symbol
            interval: Time interval
            time_period: Number of data points
            series_type: Price type
            output_format: Output format ('json' or 'csv')
            
        Returns:
            EMA data in requested format
        """
        params = {
            "function": "EMA",
            "symbol": symbol.upper(),
            "interval": interval,
            "time_period": str(time_period),
            "series_type": series_type
        }
        
        data = self.client._make_request(params)
        
        tech_key = None
        for key in data.keys():
            if "Technical Analysis" in key:
                tech_key = key
                break
        
        if not tech_key:
            raise AlphaVantageError("No technical analysis data found in response")
        
        tech_data = data[tech_key]
        
        return format_output(tech_data, output_format)
    
    def get_rsi(
        self,
        symbol: str,
        interval: str = "daily",
        time_period: int = 14,
        series_type: str = "close",
        output_format: str = "json"
    ) -> Any:
        """
        Get Relative Strength Index (RSI).
        
        Args:
            symbol: Stock symbol
            interval: Time interval
            time_period: Number of data points
            series_type: Price type
            output_format: Output format ('json' or 'csv')
            
        Returns:
            RSI data in requested format
        """
        params = {
            "function": "RSI",
            "symbol": symbol.upper(),
            "interval": interval,
            "time_period": str(time_period),
            "series_type": series_type
        }
        
        data = self.client._make_request(params)
        
        tech_key = None
        for key in data.keys():
            if "Technical Analysis" in key:
                tech_key = key
                break
        
        if not tech_key:
            raise AlphaVantageError("No technical analysis data found in response")
        
        tech_data = data[tech_key]
        
        return format_output(tech_data, output_format)
    
    def get_macd(
        self,
        symbol: str,
        interval: str = "daily",
        series_type: str = "close",
        fastperiod: int = 12,
        slowperiod: int = 26,
        signalperiod: int = 9,
        output_format: str = "json"
    ) -> Any:
        """
        Get Moving Average Convergence/Divergence (MACD).
        
        Args:
            symbol: Stock symbol
            interval: Time interval
            series_type: Price type
            fastperiod: Fast period for MACD
            slowperiod: Slow period for MACD
            signalperiod: Signal period for MACD
            output_format: Output format ('json' or 'csv')
            
        Returns:
            MACD data in requested format
        """
        params = {
            "function": "MACD",
            "symbol": symbol.upper(),
            "interval": interval,
            "series_type": series_type,
            "fastperiod": str(fastperiod),
            "slowperiod": str(slowperiod),
            "signalperiod": str(signalperiod)
        }
        
        data = self.client._make_request(params)
        
        tech_key = None
        for key in data.keys():
            if "Technical Analysis" in key:
                tech_key = key
                break
        
        if not tech_key:
            raise AlphaVantageError("No technical analysis data found in response")
        
        tech_data = data[tech_key]
        
        return format_output(tech_data, output_format)
    
    def get_bbands(
        self,
        symbol: str,
        interval: str = "daily",
        time_period: int = 20,
        series_type: str = "close",
        nbdevup: int = 2,
        nbdevdn: int = 2,
        matype: int = 0,
        output_format: str = "json"
    ) -> Any:
        """
        Get Bollinger Bands (BBANDS).
        
        Args:
            symbol: Stock symbol
            interval: Time interval
            time_period: Number of data points
            series_type: Price type
            nbdevup: Standard deviation multiplier for upper band
            nbdevdn: Standard deviation multiplier for lower band
            matype: Moving average type (0=SMA, 1=EMA, etc.)
            output_format: Output format ('json' or 'csv')
            
        Returns:
            Bollinger Bands data in requested format
        """
        params = {
            "function": "BBANDS",
            "symbol": symbol.upper(),
            "interval": interval,
            "time_period": str(time_period),
            "series_type": series_type,
            "nbdevup": str(nbdevup),
            "nbdevdn": str(nbdevdn),
            "matype": str(matype)
        }
        
        data = self.client._make_request(params)
        
        tech_key = None
        for key in data.keys():
            if "Technical Analysis" in key:
                tech_key = key
                break
        
        if not tech_key:
            raise AlphaVantageError("No technical analysis data found in response")
        
        tech_data = data[tech_key]
        
        return format_output(tech_data, output_format)
    
    def get_indicator(
        self,
        indicator: str,
        symbol: str,
        interval: str = "daily",
        output_format: str = "json",
        **kwargs
    ) -> Any:
        """
        Get any technical indicator by name.
        
        Args:
            indicator: Technical indicator function name (e.g., 'SMA', 'RSI', 'MACD')
            symbol: Stock symbol
            interval: Time interval
            output_format: Output format ('json' or 'csv')
            **kwargs: Additional parameters specific to the indicator
            
        Returns:
            Technical indicator data in requested format
        """
        indicator = indicator.upper()
        
        if indicator not in self.INDICATORS:
            available = ", ".join(sorted(self.INDICATORS.keys()))
            raise AlphaVantageError(
                f"Unknown indicator '{indicator}'. Available indicators: {available}"
            )
        
        params = {
            "function": indicator,
            "symbol": symbol.upper(),
            "interval": interval
        }
        
        # Add additional parameters
        params.update(kwargs)
        
        # Convert numeric values to strings
        for key, value in params.items():
            if isinstance(value, (int, float)):
                params[key] = str(value)
        
        data = self.client._make_request(params)
        
        tech_key = None
        for key in data.keys():
            if "Technical Analysis" in key:
                tech_key = key
                break
        
        if not tech_key:
            raise AlphaVantageError("No technical analysis data found in response")
        
        tech_data = data[tech_key]
        
        return format_output(tech_data, output_format)
    
    def list_indicators(self) -> Dict[str, str]:
        """
        Get list of available technical indicators.
        
        Returns:
            Dictionary mapping indicator codes to descriptions
        """
        return self.INDICATORS.copy()
