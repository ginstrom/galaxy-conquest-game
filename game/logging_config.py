"""Logging configuration for Galaxy Conquest game."""

import logging
import sys
from typing import Optional


def configure_logging(log_level: Optional[str] = None) -> None:
    """
    Configure logging for the game with flexible level setting.

    Args:
        log_level (str, optional): Logging level to set. 
        Defaults to INFO if not specified.
    """
    # Map string levels to logging constants
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    # Determine the log level
    if log_level:
        log_level = log_level.upper()
        if log_level not in level_map:
            print(f"Invalid log level: {log_level}. Defaulting to INFO.", 
                  file=sys.stderr)
            log_level = 'INFO'
    else:
        log_level = 'INFO'

    # Configure logging
    logging.basicConfig(
        level=level_map[log_level],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        name (str): Name of the module/component

    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)
