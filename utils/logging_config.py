"""Logging configuration for the application."""

import sys
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

import config
from config import BASE_DIR


def setup_logger():
    """Configure application-wide logging."""
    log_level = logging.DEBUG if config.config.debug else logging.INFO

    logs_dir = BASE_DIR / "logs"
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(
        logs_dir / "pastfm.log",
        maxBytes=10_485_760,
        backupCount=3,
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()