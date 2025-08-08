"""Configuration management for Alpha Vantage CLI."""

import os
from pathlib import Path
from configparser import ConfigParser
from typing import Optional, Any, Union


class Config:
    """Configuration manager for Alpha Vantage CLI."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file. If not provided,
                        will look for config.ini in current directory.
        """
        self.config = ConfigParser()
        
        # Default configuration
        self.config.read_dict({
            "DEFAULT": {
                "base_url": "https://www.alphavantage.co/query",
                "rate_limit_delay": "12.0",
                "output_format": "json",
                "timeout": "30.0",
            }
        })
        
        # Load configuration file
        self._load_config_file(config_file)
    
    def _load_config_file(self, config_file: Optional[str]) -> None:
        """
        Load configuration from file.
        
        Args:
            config_file: Path to configuration file
        """
        if config_file:
            config_path = Path(config_file)
        else:
            # Look for config.ini in current directory
            config_path = Path("config.ini")
        
        if config_path.exists():
            try:
                self.config.read(config_path)
            except Exception as e:
                # If config file is malformed, continue with defaults
                print(f"Warning: Failed to read config file {config_path}: {e}")
    
    def get(self, key: str, default: Any = None, section: str = "DEFAULT") -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            section: Configuration section
            
        Returns:
            Configuration value
        """
        try:
            return self.config.get(section, key)
        except Exception:
            return default
    
    def get_bool(self, key: str, default: bool = False, section: str = "DEFAULT") -> bool:
        """
        Get boolean configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            section: Configuration section
            
        Returns:
            Boolean configuration value
        """
        try:
            return self.config.getboolean(section, key)
        except (KeyError, ValueError):
            return default
    
    def get_int(self, key: str, default: int = 0, section: str = "DEFAULT") -> int:
        """
        Get integer configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            section: Configuration section
            
        Returns:
            Integer configuration value
        """
        try:
            return self.config.getint(section, key)
        except (KeyError, ValueError):
            return default
    
    def get_float(self, key: str, default: float = 0.0, section: str = "DEFAULT") -> float:
        """
        Get float configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            section: Configuration section
            
        Returns:
            Float configuration value
        """
        try:
            return self.config.getfloat(section, key)
        except (KeyError, ValueError):
            return default
    
    def set(self, key: str, value: Any, section: str = "DEFAULT") -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
            section: Configuration section
        """
        if section != "DEFAULT" and not self.config.has_section(section):
            self.config.add_section(section)
        
        self.config.set(section, key, str(value))
    
    def save(self, config_file: str) -> None:
        """
        Save configuration to file.
        
        Args:
            config_file: Path to configuration file
        """
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            self.config.write(f)
    
    def sections(self) -> list:
        """Get list of configuration sections."""
        return self.config.sections()
    
    def has_section(self, section: str) -> bool:
        """Check if configuration section exists."""
        return self.config.has_section(section)
    
    def has_option(self, key: str, section: str = "DEFAULT") -> bool:
        """Check if configuration option exists."""
        return self.config.has_option(section, key)
