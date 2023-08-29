import logging


class Log:
    _logger = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger is None:
            logger = logging.getLogger(__name__)
            format = '%(asctime)s:%(levelname)s: %(message)s'
            logging.basicConfig(level=logging.INFO, format=format)
            cls._logger = logger
        return cls._logger

    @classmethod
    def info(cls, message):
        cls.get_logger().info(message)

    @classmethod
    def debug(cls, message):
        cls.get_logger().debug(message)

    @classmethod
    def warning(cls, message):
        cls.get_logger().warning(message)

    @classmethod
    def error(cls, message):
        cls.get_logger().error(message)
