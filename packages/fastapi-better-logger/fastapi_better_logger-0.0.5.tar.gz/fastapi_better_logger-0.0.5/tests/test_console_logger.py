import logging
import logging.config

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi_better_logger import (
    DEFAULT_CONFIG
)

logging.config.dictConfig(DEFAULT_CONFIG)


def log_from_logger(args=None):
    if args is None:
        args = {}
    logger = logging.getLogger("uvicorn.access")
    assert len(logger.handlers) == 1
    logger.debug("Debug message", args)
    logger.info("Info message", args)
    logger.warning("Warning message", args)
    logger.error("Error message", args)
    logger.critical("Critical ", args)


def log_from_logger_na():
    logger = logging.getLogger("uvicorn")
    assert len(logger.handlers) == 1
    logger.debug("Debug message ", )
    logger.info("Info message", )
    logger.warning("Warning message", )
    logger.error("Error message", )
    logger.critical("Critical ", )


def test_logger_console():
    log_from_logger_na()

    log_from_logger_na()

    log_from_logger(
        {"client_addr": "ssaaaa", "method": "GET", "full_path": "/", "http_version": "1.1", "status_code": 200})


test_logger_console()
