import logging


class Worker:
    def __init__(self, config, overide_logger=None):
        if overide_logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = overide_logger
        self.config = config

    def log_something(self, msg):
        self.logger.debug(f"debug msg: {msg}")
        self.logger.info(f"info msg: {msg}")
        self.logger.warning(f"warning msg: {msg}")
        self.logger.error(f"error msg: {msg}")
        self.logger.critical(f"critical msg: {msg}")
