#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging


def init_logging(log_level=0):
    """
    Initialize the logging framework.
    """
    # Configure logging.
    root_logger = logging.getLogger(__name__)

    # formater_base = '%(asctime)s [%(levelname)s]:[%(threadName)s] %(message)s'
    formater_base = '%(asctime)s [%(levelname)s] %(message)s'
    log_formatter = logging.Formatter(formater_base)
    # Log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    # Append the logs and overwrite once reached 1MB
    if log_level == 1:
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(console_handler)
        root_logger.propagate = False
    elif log_level >= 2:
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(console_handler)
        # Log to file
        # file_handler = RotatingFileHandler(
        #     config_base.LOG_FILE_PATH, maxBytes=1024 * 1024, backupCount=5, encoding=None, delay=0)
        # file_handler.setFormatter(log_formatter)
        # root_logger.addHandler(file_handler)
    else:
        root_logger.setLevel(logging.WARN)
        root_logger.addHandler(console_handler)

    return root_logger
