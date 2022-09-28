"""
common.logger

Logger Class File
"""

import logging
import sys
from pathlib import Path


# Define logs directory
LOG_DIR = Path(__file__).resolve().parents[1].joinpath("logs")

# Cache all instantiated loggers
loggers: dict[str, logging.Logger] = {}


# pylint: disable = too-many-instance-attributes, too-many-arguments, too-few-public-methods
# Logger Class needs to have many instance attributes for modularity
class Logger:
    """
    Custom Logging Class
    """

    def __init__(
        self,
        name: str,
        file_handler: bool = True,
        stream_handler: bool = True,
        level: int = logging.DEBUG,
        file_level: int = None,
        stream_level: int = None,
    ) -> None:
        """
        Logger Class Constructor

        Parameters
        ----------
        name : str
            Logger Name

        file_handler : bool, optional
            Add File Handler, by default True.

        stream_handler : bool, optional
            Add Stream Handler, by default True.

        level : int, optional
            Logger Level, by default logging.DEBUG.

        file_level : int, optional
            File Handler Level, by default None.
            Inherits from Logger Level if None.

        stream_level : int, optional
            Stream Handler Level, by default None.
            Inherits from Logger Level if None.

        Returns None
        """

        # Parameters
        self.name: str = name
        self.add_file_handler: bool = file_handler
        self.add_stream_handler: bool = stream_handler
        self.file_level: int = file_level if file_level else level
        self.stream_level: int = stream_level if stream_level else level
        self.level: int = min(self.file_level, self.stream_level)

        # Get root name if name is child
        self.root_name = self.name.split(".")[0]

        # Define log filename path
        self.filename: Path = LOG_DIR.joinpath(f"{self.root_name}.log")
        self.__create_log_file()

        # Define Format
        self.format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.formatter: logging.Formatter = logging.Formatter(self.format)

        # Get logger
        self._logger: logging.Logger = self.get_logger()

    def get_logger(self) -> logging.Logger:
        """
        Get the logger
        """

        # Check if logger already exists
        if self.name in loggers:
            logger = loggers[self.name]
            logger.info(f"Getting logger: {self.name}")

        # Create logger
        else:
            logger = self.__create_logger()
            logger.info("Creating logger: %s", self.name)

            # Cache logger
            loggers[self.name] = logger
            logger.info("Caching logger: %s", self.name)

        return logger

    def __create_logger(self) -> logging.Logger:
        """
        Create the logger and add handlers
        """

        # Create logger
        logger = logging.getLogger(self.name)

        # Do not propagate to root logger
        logger.propagate = False

        # Define logger level
        logger.setLevel(self.level)

        # Add File and Stream Handlers
        self.__add_handlers(logger)

        return logger

    def __create_log_file(self) -> None:
        """
        Create Log File
        """

        # Check if logs directory exists
        if not LOG_DIR.exists():
            LOG_DIR.mkdir()

        # Check if log file exists
        if not self.filename.exists():
            self.filename.touch()

    def __add_handlers(self, logger: logging.Logger) -> None:
        """
        Add File and Stream Handlers
        :param logger: Logger object
        :return None
        """

        # Get all handlers already added to logger
        _file_handlers = [
            handler
            for handler in logger.handlers
            if isinstance(handler, logging.FileHandler)
        ]
        _stream_handlers = [
            handler
            for handler in logger.handlers
            if isinstance(handler, logging.StreamHandler)
        ]

        # Add File Handler if not already added and requested
        if self.add_file_handler and _file_handlers == []:
            logger.addHandler(self.__create_file_handler())

        # Add Stream Handler if not already added and requested
        if self.add_stream_handler and _stream_handlers == []:
            logger.addHandler(self.__create_stream_handler())

    def __create_file_handler(self) -> logging.FileHandler:
        """
        Create File Handler
        :return: File Handler Object
        """

        file_handler = logging.FileHandler(filename=self.filename)
        file_handler.setLevel(self.file_level)
        file_handler.setFormatter(self.formatter)

        return file_handler

    def __create_stream_handler(self) -> logging.StreamHandler:
        """
        Create Stream Handler
        :return: Stream Handler Object
        """

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(self.stream_level)
        stream_handler.setFormatter(self.formatter)

        return stream_handler
