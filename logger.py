import logging
import os
from datetime import date
from logging.handlers import TimedRotatingFileHandler

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)


def setup_logging():
    # Create a timed rotating file handler
    current_date = date.today().strftime("%Y-%m-%d")
    log_file_pattern = os.path.join(LOGS_DIR, f"fastapi_app_{current_date}.log")
    file_handler = TimedRotatingFileHandler(
        log_file_pattern, when="midnight", interval=1, backupCount=0
    )

    # Set the logging level and format
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s - %(funcName)s - %(lineno)d - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Create a logger and add the file handler
    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    return logger
