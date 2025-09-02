from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(log_file: str = "logs/bot.log") -> logging.Logger:
    """Configure application wide logger.

    Parameters
    ----------
    log_file: str
        Path to the log file.
    """
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[handler],
    )
    return logging.getLogger("iherb_bot")
