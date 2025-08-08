#!/usr/bin/env python3
"""Setup script for alphavantage-cli package."""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Alpha Vantage CLI - Command-line interface for Alpha Vantage API"

setup(
    name="alphavantage-cli",
    version="1.0.0",
    author="Alpha Vantage CLI Team",
    author_email="support@example.com",
    description="Python package and CLI for Alpha Vantage financial market data API",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/example/alphavantage-cli",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "click>=8.0.0",
        "pandas>=1.5.0",
        "configparser>=5.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "alphavantage=alphavantage_cli.cli:cli",
            "av=alphavantage_cli.cli:cli",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/example/alphavantage-cli/issues",
        "Source": "https://github.com/example/alphavantage-cli",
        "Documentation": "https://alphavantage-cli.readthedocs.io/",
    },
)
