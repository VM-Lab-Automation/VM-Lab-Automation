import logging
import os


def get_logger(name):
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    return logging.getLogger(name)
