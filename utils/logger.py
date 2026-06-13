"""Centralized logging setup for Student Study Buddy."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import LOG_DATE_FORMAT, LOG_DIR, LOG_FORMAT, LOG_LEVEL

_loggers: dict[str, logging.Logger] = {}


def setup_logger(name: str) -> logging.Logger:
    """Create and configure a logger with file and console handlers.

    Uses a rotating file handler (5MB max, 3 backups) and a console handler.
    Loggers are cached by name to avoid duplicate handlers.

    Args:
        name: Logger name (typically module name).

    Returns:
        Configured Logger instance.
    """
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    logger.propagate = False

    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    log_file = Path(LOG_DIR) / "app.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    _loggers[name] = logger
    return logger
