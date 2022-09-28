"""
browser.webdriver

WebDriver Class File
"""

import logging
from pathlib import Path

import dotenv
import psutil
from selenium.webdriver.firefox.service import Service
from webdriver_manager.core import logger as webdriver_manager_logger
from webdriver_manager.firefox import GeckoDriverManager

from common.logger import Logger, LOG_DIR

# Load environment variables
dotenv.load_dotenv()

# Create logger
wdm_logger = Logger(
    "webdriver_manager",
    file_handler=True,
    stream_handler=True,
    level=logging.NOTSET,
    file_level=logging.DEBUG,
    stream_level=logging.ERROR,
)

wdm_log_path: Path = LOG_DIR.joinpath("webdriver_manager.log")

# Bind logger to webdriver_manager
# pylint: disable=protected-access
# No other way to set custom logger
# https://github.com/SergeyPirogov/webdriver_manager/pull/439
webdriver_manager_logger.__logger = wdm_logger.get_logger()


class WebDriver:
    """
    WebDriver Class
    """

    webdriver_log_path: Path = LOG_DIR.joinpath("webdriver.log")

    # Create webdriver.log if it doesn't exist
    if not webdriver_log_path.exists():
        webdriver_log_path.touch()

    def __init__(self, install: bool = True) -> None:
        """
        Constructor

        Parameters
        ----------
        install : bool, optional
            Install Gecko Driver, by default True.
        """

        self.driver_manager: GeckoDriverManager = GeckoDriverManager()
        self.driver_path: str | None = None

        if install:
            self.install()
        else:
            # pylint: disable=protected-access
            # Accessing private method is the only way to get the path without installing
            # NOTE: this assumes the driver install path is cached
            # If it is not, the driver will be installed
            self.driver_path = self.driver_manager._get_driver_path(
                driver=self.driver_manager.driver
            )

    @property
    def service(self):
        """
        Get Service Object

        Returns
        -------
        selenium.webdriver.firefox.service.Service : Firefox Service Object
        """

        return Service(self.driver_path, log_path=str(self.webdriver_log_path))

    def install(self) -> str:
        """
        Install Gecko Driver

        Returns
        -------
        str : Gecko Driver Path

        Notes
        -----
        This method updates the driver_path attribute.
        """

        install_path = self.driver_manager.install()

        # Update cached driver path
        self.driver_path = install_path

        return install_path

    def uninstall(self, force: bool = False, retry: int = 3) -> None:
        """
        Uninstall Gecko Driver

        Parameters
        ----------
        force : bool, optional
            Force uninstall, by default False
            Kills all processes locking the driver file.
        retry : int, optional
            Number of retries, by default 3
            Requires force to be True.
        """

        driver_path = Path(self.driver_path)

        # Check if driver is installed
        if not driver_path.exists():
            return

        for _ in range(retry):
            try:
                if force:
                    # Kill all processes locking the driver file
                    for process in psutil.process_iter():
                        if "geckodriver" in str(process.name()).lower():
                            process.kill()

                # Uninstall driver
                driver_path.unlink()
                return

            except PermissionError:
                # Do not force uninstall
                if not force:
                    raise
