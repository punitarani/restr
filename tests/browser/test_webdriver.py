"""
tests.browser.test_webdriver.py

Filename does not have a test prefix as it is meant to be run in test_browser.py not standalone.
"""

import pytest
from pathlib import Path

from restr.browser.webdriver import WebDriver, wdm_log_path


@pytest.mark.order(1)
class TestWebDriver:
    """Test WebDriver"""

    def test_init(self):
        """Test Init"""

        driver = WebDriver(install=False)

        # Verify logs directory is correct and exists
        assert driver.webdriver_log_path.resolve().parts[-3:] == (
            "restr",
            "logs",
            "webdriver.log",
        )

        # Check if the log files exist
        assert wdm_log_path.exists()
        assert driver.webdriver_log_path.exists()

    def test_install(self):
        """Test Install"""

        # Install driver
        driver = WebDriver(install=False)

        # Verify DriverManager._get_driver_path() is working
        assert driver.driver_path

        # Verify driver is installed
        driver.install()
        assert Path(driver.driver_path).exists()

    def test_uninstall(self):
        """Test Uninstall"""

        driver = WebDriver(install=True)
        assert Path(driver.driver_path).exists()

        # Verify driver is uninstalled
        driver.uninstall(force=False)
        assert not Path(driver.driver_path).exists()
