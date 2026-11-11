"""
Centralized logging configuration for AgriSense AI.
Provides clean, structured logging across all backend modules.
"""

import logging
import sys


def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """Configure centralized logger with clean console formatting."""
    logger = logging.getLogger("agrisense")
    if not logger.handlers:
        logger.setLevel(log_level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger


logger = setup_logging()
