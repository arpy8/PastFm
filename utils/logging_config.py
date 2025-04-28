"""Logging configuration for the application."""

import sys
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Change relative import to absolute import
import config
from config import BASE_DIR


def setup_logger():
    """Configure application-wide logging."""
    log_level = logging.DEBUG if config.config.debug else logging.INFO
    
    # Create logs directory if it doesn't exist
    logs_dir = BASE_DIR / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatters
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    
    # Create file handler for all logs
    file_handler = RotatingFileHandler(
        logs_dir / "pastfm.log",
        maxBytes=10_485_760,  # 10MB
        backupCount=3
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Initialize logger when imported
logger = setup_logger()
