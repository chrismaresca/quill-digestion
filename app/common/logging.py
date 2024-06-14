# app/logging_config.py
import logging

def setup_logging():
    FORMAT = "%(levelname)s:\t%(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)

setup_logging()
