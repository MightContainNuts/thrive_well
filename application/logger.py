import logging
import sys
from pathlib import Path


def setup_logger(name: str) -> logging.Logger:
    """
    Creates and configures a logger that writes to both a log file and stdout
    (for Heroku logs).
    :param name: Logger name, usually `__name__`.
    :return: Configured logger instance.
    """
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    logger = logging.getLogger(name)
    if not logger.hasHandlers():  # Avoid duplicate handlers
        logger.setLevel(logging.INFO)

        # File handler (for local logs)
        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setLevel(logging.INFO)

        # Log format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        # Stream handler (for Heroku logs)
        stream_handler = logging.StreamHandler(sys.stdout)  # Log to stdout
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        # Add both handlers
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
