import logging

from loguru import logger


class Logger:
    def __init__(self, log_level: str):
        logging.basicConfig()
        logging.getLogger("urllib3").setLevel(logging.ERROR)

        logger.level(log_level)

        self.logger = logger


