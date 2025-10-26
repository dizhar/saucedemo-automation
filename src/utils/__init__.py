"""
Utilities Package

This package contains utility modules for the test automation framework.

Modules:
- config.py: Configuration management and environment variables
- logger.py: Logging setup and configuration

Usage:
    from src.utils.config import config
    from src.utils.logger import logger
    
    # Or use package-level imports:
    from src.utils import config, logger
"""

from .config import config
from .logger import logger

__all__ = ['config', 'logger']