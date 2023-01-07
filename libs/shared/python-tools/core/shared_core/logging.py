"""Logging module."""

import logging
import os

from pythonjsonlogger import jsonlogger


def setup_logging(
    module_name: str,
    propagate: bool = False,
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
) -> logging.Logger:
    """
    Set up logging using JSON format.

    Args:
        module_name (str): The module name.
        propagate (bool): Whether to propagate the logging to the parent logger.
        log_level (str): The log level.

    Returns:
        The logger.
    """
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter("%(levelname)s %(message)s ")
    log_handler.setFormatter(formatter)

    logger = logging.getLogger(module_name)
    logger.addHandler(log_handler)
    logger.propagate = propagate
    logger.setLevel(logging.getLevelName(log_level))
    return logger
