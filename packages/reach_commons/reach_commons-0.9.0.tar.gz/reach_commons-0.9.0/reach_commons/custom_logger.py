import json
import logging
import os
import uuid


class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class SingletonLogger(metaclass=Singleton):
    logger = logging.getLogger()
    logger.setLevel(os.environ.get("logger_level") or logging.INFO)
    context = {"logger_identifier": "reach_logger"}

    def set_context(self, **kwargs):
        self.context = {"logger_identifier": "reach_logger", **kwargs}

    def _log(self, level, msg, *args, **kwargs):
        log_message = {"level": str(level), **self.context, "message": str(msg)}
        self.logger.log(level, json.dumps(log_message), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log(logging.INFO, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log(logging.ERROR, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log(logging.WARNING, msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self._log(logging.ERROR, msg, *args, **kwargs)

    # noinspection PyPep8Naming
    def setLevel(self, level: str):
        self.logger.setLevel(level=level or logging.INFO)


logger = SingletonLogger()


def set_business_id(business_id, pos_partner, level=logging.INFO):
    logger.set_context(business=business_id, partner=pos_partner)
    logger.setLevel(level)


def get_logger():
    return logger
