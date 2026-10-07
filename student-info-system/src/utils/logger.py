"""Logging setup: rotating file handler + console warnings."""
import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(log_cfg: dict) -> logging.Logger:
    """Create the application logger from the logging config section."""
    logger = logging.getLogger("sis")
    if logger.handlers:          # avoid duplicate handlers on re-init
        return logger

    level = getattr(logging, str(log_cfg.get("level", "INFO")).upper(),
                    logging.INFO)
    logger.setLevel(level)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")

    log_file = log_cfg.get("file", "logs/app.log")
    os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=log_cfg.get("max_bytes", 1048576),
        backupCount=log_cfg.get("backup_count", 3),
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)   # keep the menu UI clean
    console.setFormatter(fmt)
    logger.addHandler(console)
    return logger
