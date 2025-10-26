"""
Simple logger configuration for test automation.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from src.utils.config import config
from typing import Optional


def setup_logger(name: str = __name__, log_level: Optional[str] = None) -> logging.Logger:
    """
    Setup and configure logger
    
    Args:
        name: Logger name
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Get log level from config or parameter
    level = log_level or config.LOG_LEVEL
    log_level_obj = getattr(logging, level.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level_obj)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(config.LOG_FORMAT)
    
    # Console handler
    if config.LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level_obj)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if config.LOG_TO_FILE:
        log_file = config.get_log_file_path()
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(log_level_obj)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Create default logger
logger = setup_logger("test_automation")