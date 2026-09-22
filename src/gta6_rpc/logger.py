"""Application logging configuration."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .models import LoggingConfig


def configure_logging(config: LoggingConfig) -> None:
    path = Path(config.file)
    if not path.is_absolute():
        path = Path.cwd() / path
    path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, config.level, logging.INFO))
    if any(
        isinstance(handler, RotatingFileHandler)
        and Path(getattr(handler, "baseFilename", "")) == path.resolve()
        for handler in logger.handlers
    ):
        return
    handler = RotatingFileHandler(
        path, maxBytes=config.max_bytes, backupCount=config.backup_count, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    logger.addHandler(handler)
