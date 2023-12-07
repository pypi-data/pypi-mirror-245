import logging
import os

from cast_ai.se.constants import LOG_DIR


def setup_logging(logger_name, log_level: str = logging.INFO) -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)
    created_logger = logging.getLogger(logger_name)
    created_logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s - %(message)s')
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, 'all_logs.log'))
    file_handler.setFormatter(formatter)
    created_logger.addHandler(file_handler)
    created_logger.propagate = False
    return created_logger
