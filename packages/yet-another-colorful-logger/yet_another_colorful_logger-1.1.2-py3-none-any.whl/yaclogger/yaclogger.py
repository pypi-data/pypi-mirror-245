import logging
from sys import exit

from colorlog import ColoredFormatter, StreamHandler, getLogger
from colorlog.escape_codes import parse_colors


class YACLogger:
    """
    Yet Another Colorful Logger is just another Python colorful logger that uses adds color to console log messages based on their severity level.

    Attributes:
        DEBUG (int): Debug level from the logging module.
        INFO (int): Info level from the logging module.
        WARNING (int): Warning level from the logging module.
        ERROR (int): Error level from the logging module.
        CRITICAL (int): Critical level from the logging module.
        logger (Logger): An instance of a logger with a specific name and color formatting.
    """

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(self,name: str = "",level: str = logging.DEBUG,
                 log_colors: dict = { "debug": "", "info": "", "warning": "", "error": "", "critical": ""}):
        """
        Initialize the YACLogger.

        Args:
            name (str): The name of the logger.
            level (int): The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL). Default is DEBUG.
            log_colors_dict (dict): A dictionary of colors for each logging level. Default is an empty dictionary.
        """
        supported_levels = ["debug", "info", "warning", "error", "critical"]
        assert isinstance(log_colors, dict), "The parameter log_colors must be a dictionary"
        if not any(key in supported_levels for key in log_colors.keys()): raise KeyError(f"Invalid log_colors parameter")
        log_colors = {key: value for key, value in log_colors.items() if key in supported_levels}
        for key, value in log_colors.items():
            try:
                parse_colors(value)
            except:
                raise ValueError(f"Invalid color '{value}' for log level '{key}'")                
        style = (
            "%(log_color)s[%(asctime)s.%(msecs)05ds]"
            "[%(threadName)s]"
            "[%(name)s] %(message)s"
        )
        formatter = ColoredFormatter(
            style,
            datefmt="%d/%m/%Y][%H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": log_colors.get("debug","") or "cyan",
                "INFO": log_colors.get("info","") or "white",
                "WARNING": log_colors.get("warning","") or "yellow",
                "ERROR": log_colors.get("error","")or "bold_red",
                "CRITICAL": log_colors.get("critical","")or "white,bg_red",
            },
            secondary_log_colors={},
            style="%",
        )

        self.logger = getLogger(name)
        if len(self.logger.handlers) == 0 and name:
            handler = StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.set_level(level)

    def set_level(self, level):
        """
        Set the logging level.

        Args:
            level (int): The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        """
        self.logger.setLevel(level)

    def debug(self, formatter, *args):
        """
        Log a debug message.

        Args:
            formatter (str): The log message format.
            args: Values to format into the message.
        """
        self.logger.debug(formatter.format(*args))

    def info(self, formatter, *args):
        """
        Log an info message.

        Args:
            formatter (str): The log message format.
            args: Values to format into the message.
        """
        self.logger.info(formatter.format(*args))

    def warning(self, formatter, *args):
        """
        Log a warning message.

        Args:
            formatter (str): The log message format.
            args: Values to format into the message.
        """
        self.logger.warning(formatter.format(*args))

    def error(self, formatter, *args):
        """
        Log an error message.

        Args:
            formatter (str): The log message format.
            args: Values to format into the message.
        """
        self.logger.error(formatter.format(*args))

    def critical(self, formatter, *args):
        """
        Log a critical message and exit with status code -1.

        Args:
            formatter (str): The log message format.
            args: Values to format into the message.
        """
        self.logger.critical(formatter.format(*args))
        exit(-1)
