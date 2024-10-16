""" Logging configuration"""

import logging
import os


logger = logging.getLogger(__name__)


def set_logging():
    log_level = os.environ.get("LOG_LEVEL", "WARNING")

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)-20s %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    handlers = [console_handler]

    log = logging.getLogger("root")
    log.setLevel(log_level)
    for handler in handlers:
        log.addHandler(handler)

    logger.debug(f"Logging configured, verbosity: {log_level}")
