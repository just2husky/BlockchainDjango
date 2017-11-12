from logging.config import fileConfig
import logging
import os.path


class Logger:
    logger_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'logger_config.ini')
    fileConfig(logger_config_file)
    logger = logging.getLogger('infoLogger')

    @classmethod
    def info(cls, msg):
        cls.logger.info(msg)
