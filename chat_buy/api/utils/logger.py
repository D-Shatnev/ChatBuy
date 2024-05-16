"""
This module contains functions for working with logging.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOGS_DIR = os.getenv("LOGS_DIR", "logs/")


def get_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    Create and configure a logger with the given name and log level.

    Args:
        name (str): The name of the logger.
        level (int, optional): The log level for the logger. Defaults to logging.INFO.

    Returns:
        logging.Logger: The configured logger.
    """
    if not Path(LOGS_DIR).is_dir():
        Path(LOGS_DIR).mkdir(parents=True)
    file_path = Path(LOGS_DIR) / f"{name}.log"
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = RotatingFileHandler(file_path.as_posix(), maxBytes=2097152, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s [in %(pathname)s:%(lineno)d]")
        )
        file_handler.setLevel(level)
        logger.addHandler(file_handler)
    return logger
