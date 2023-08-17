import logging


class Log:
    _logger = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger

    @classmethod
    def info(cls, message):
        cls.get_logger().info(message)
