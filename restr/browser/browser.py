"""
restr.browser.browser

Browser Class File
Handles browser window and tab instances
"""

from selenium.webdriver import Firefox, FirefoxOptions

from restr.browser.webdriver import WebDriver
from restr.browser.window import Window
from restr.browser.browser_base import BrowserBase


class Browser(BrowserBase):
    """
    Browser Class
    """

    def __init__(self, *args, headless: bool = False, **kwargs) -> None:
        """
        Constructor

        Parameters
        ----------
        headless : bool, optional
            Run browser in headless mode, by default False

        Notes
        -----
        This method will open a new browser window with a blank page.
        """

        super().__init__(*args, **kwargs)

        # Create WebDriver instance
        self.driver: WebDriver = WebDriver()

        # Define browser options
        self.options = FirefoxOptions()
        self.options.headless = headless
        self.options.add_argument("--disable-blink-features=AutomationControlled")

        # Set User Agent to Firefox
        self.options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
        )

        # Create browser
        self.browser: Firefox = Firefox(
            service=self.driver.service, options=self.options
        )

        # Store Window instances
        self.windows: dict[str, Window] = {
            self.browser.current_window_handle: Window(
                browser=self.browser, handle=self.browser.current_window_handle
            )
        }

    # pylint: disable=arguments-differ
    # Overriding method from BrowserBase
    def open(self, url: str = None) -> str:
        """
        Open Browser

        Parameters
        ----------
        url : str, optional
            Link to open, by default None.
            If None, then a blank page will be opened.

        Returns
        -------
        str: Browser Window Handle
        """

        # Format url if provided. Set open blank page if not.
        url = self._format_url(url) if url else "about:blank"

        # Open an empty browser
        self.browser.get(url)

        # Create Window instance
        window_handle = self.browser.current_window_handle
        window = Window(handle=window_handle, browser=self.browser)

        # Store Window instance
        self.windows[window_handle] = window

        return window_handle

    # pylint: disable=arguments-differ
    # Overriding method from BrowserBase
    def close(self) -> None:
        """Close Browser"""

        self.browser.quit()
