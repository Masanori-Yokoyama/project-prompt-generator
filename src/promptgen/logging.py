"""Logging configuration for the promptgen package."""

import logging
import sys
from typing import Optional

LOGGER = logging.getLogger("promptgen")


def setup_logging(level: Optional[str] = None) -> None:
    """Configure logging for the promptgen package.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    if level is None:
        level = "INFO"

    # 既存のハンドラをクリア
    LOGGER.handlers.clear()

    # ハンドラの設定
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

    LOGGER.addHandler(handler)

    try:
        LOGGER.setLevel(getattr(logging, level.upper()))
    except AttributeError:
        LOGGER.setLevel(logging.INFO)
