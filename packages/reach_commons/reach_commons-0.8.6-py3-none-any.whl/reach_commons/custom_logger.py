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


# noinspection PyPep8Naming
class SingletonLogger(metaclass=Singleton):
    logger = logging.getLogger()
    logger.setLevel(os.environ.get("logger_level") or logging.INFO)
    context = {}

    def set_context(self, **kwargs):
        self.context = kwargs

    def _log(self, level, msg, *args, **kwargs):
        kwargs.update(self.context)
        self.logger.log(level, msg, *args, **kwargs)

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

    def setLevel(self, level: str):
        self.logger.setLevel(level=level or logging.INFO)


logger = SingletonLogger()


def set_business_id(business_id, pos_partner, level=logging.INFO):
    logger.set_context(business_id=business_id, pos_partner=pos_partner)
    logger.setLevel(level)


def get_logger():
    return logger
