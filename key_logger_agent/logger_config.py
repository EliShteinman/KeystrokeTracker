import sys
import logging
from logging.handlers import RotatingFileHandler
from config import Config

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("KeyLoggerAgent")
    if logger.hasHandlers():
        return logger

    logger.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))
    formatter = logging.Formatter(Config.LOG_FORMAT)

    file_handler = RotatingFileHandler(
        Config.LOG_FILE, maxBytes=5*1024*1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if Config.TESTING_MODE:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()
