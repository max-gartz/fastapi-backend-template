"""Module for logging utilities."""
import functools
import logging
import logging.config
from typing import Any, Dict

import yaml


@functools.cache
def get_logging_config(config_path: str) -> Dict[str, Any]:
    """Get logging configuration."""
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def setup_logging(config_path: str) -> None:
    """Setup logging."""
    log_config = get_logging_config(config_path=config_path)
    logging.config.dictConfig(log_config)


def shutdown_logging() -> None:
    """Shutdown logging."""
    logger = logging.getLogger()
    logger.info("Shutting down...")
    logging.shutdown(logger.handlers)
