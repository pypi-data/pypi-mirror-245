import logging
import os

from graypy import GELFTLSHandler


def get_default_log(instance_name):
    logger = logging.getLogger(f"crawling_{instance_name}_log")
    logger.setLevel(logging.INFO)

    if os.getenv("GRAYLOG_ENABLE") == "TRUE":
        handler = GELFTLSHandler(os.getenv("GRAYLOG_ADDR"), os.getenv("GRAYLOG_PORT"))
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler())

    return logger
