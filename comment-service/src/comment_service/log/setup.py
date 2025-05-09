from logging.handlers import TimedRotatingFileHandler
from fastapi.logger import logger as fastapi_logger
from globals import LOGS_LEVEL, LOGS_FILENAME, LOGS_FORMAT
from datetime import datetime
import logging
import sys
import os

def setup_logging():
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers.clear()

    formatter = logging.Formatter(LOGS_FORMAT)

    # Simple console/stdout logging
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)

    # File logging handler
    os.makedirs("logs", exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        LOGS_FILENAME.format(date=datetime.now().strftime('%Y-%m-%d')),
        when="midnight",
        interval=1,
        backupCount=7
    )
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(LOGS_LEVEL)
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    fastapi_logger.handlers = logger.handlers
    fastapi_logger.setLevel(LOGS_LEVEL)
