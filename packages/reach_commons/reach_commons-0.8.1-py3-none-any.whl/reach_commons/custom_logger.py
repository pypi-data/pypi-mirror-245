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
    context_string = "reach_custom_logger: "

    def set_context(self, extra: str):
        self.context_string = f"{self.context_string}{extra}"

    def info(self, msg, *args, **kwargs):
        self.logger.info(self.context_string + " " + msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(self.context_string + " " + msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(self.context_string + " " + msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(self.context_string + " " + msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(self.context_string + " " + msg, *args, **kwargs)

    # noinspection PyPep8Naming
    def setLevel(self, level: str):
        self.logger.setLevel(level=level or logging.INFO)


logger = SingletonLogger()


def set_business_id(business_id, pos_partner, level=logging.INFO):
    logger.set_context(
        f"[Request: {uuid.uuid4()}][Business: {business_id}][Partner: {pos_partner}]"
    )
    logger.setLevel(level)


def get_logger():
    return logger
