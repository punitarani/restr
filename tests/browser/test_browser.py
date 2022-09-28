"""tests.browser.test_browser.py"""

import pytest

from restr.browser.browser import Firefox
from restr.browser.browser_base import BrowserBase
from restr.browser.webdriver import WebDriver
from restr.browser.window import Window


class TestBrowserBase:
    """Test BrowserBase"""

    def test_init(self):
        """Test __init__()"""
        browserbase = BrowserBase()
        assert pytest.raises(NotImplementedError, browserbase.open)
        assert pytest.raises(NotImplementedError, browserbase.close)

    def test_format_url(self):
        """Test _format_url()"""
        # pylint: disable=protected-access
        # Testing protected method
        assert BrowserBase._format_url("icann.org/") == "https://icann.org/"


class TestBrowser:
    """
    Test Browser
    """

    def test_init(self, browser):
        """
        Test Init
        """

        # Verify initializations
        assert isinstance(browser.driver, WebDriver)
        assert isinstance(browser.browser, Firefox)

        # Verify browser is open and has a window
        assert browser.browser.current_window_handle in browser.windows
        assert isinstance(
            browser.windows[browser.browser.current_window_handle], Window
        )

        # Close browser
        browser.browser.quit()

        # Verify browser is closed
        assert browser.browser.service.process is None

    def test_open_close(self, browser):
        """
        Test Open and Close
        """

        # Open a new window
        window_handle = browser.open(url="https://www.icann.org/")

        # Verify window is open
        assert window_handle in browser.windows
        assert isinstance(browser.windows[window_handle], Window)

        # Verify window url is correct
        assert (
                browser.windows[window_handle].browser.current_url
                == "https://www.icann.org/"
        )

        # Close browser
        browser.close()

        # Verify browser is closed
        assert browser.browser.service.process is None
