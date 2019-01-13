""" See https://docs.python.org/3/howto/logging.html for usage. """
import logging

def setup_custom_logger(logger, log_level="INFO"):
    datefmt = '%d-%m-%Y %H:%M:%S '
    fmt = '%(asctime)-15s %(levelname)5s %(module)s  %(message)s'
    formatter = logging.Formatter(fmt, datefmt)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(handler)
