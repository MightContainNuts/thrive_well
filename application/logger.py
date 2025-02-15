import logging
from pathlib import Path


def setup_logger(name: str) -> logging.Logger:
    """
    Creates and configures a logger that writes to a central log file.
    :param name: Logger name, usually `__name__`.
    :return: Configured logger instance.
    """
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    logger = logging.getLogger(name)
    if not logger.hasHandlers():  # Avoid duplicate handlers
        logger.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setLevel(logging.INFO)

        # Log format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
