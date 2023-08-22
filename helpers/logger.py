import logging


class Log:
    _logger = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            cls._logger = logger
        return cls._logger

    @classmethod
    def info(cls, message):
        cls.get_logger().info(message)

    @classmethod
    def warning(cls, message):
        cls.get_logger().warning(message)

    @classmethod
    def error(cls, message):
        cls.get_logger().error(message)
