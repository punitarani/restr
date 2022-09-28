"""
restr.browser.window

Window Class File
"""

from selenium.webdriver import Firefox
from restr.browser.browser_base import BrowserBase


class Window(BrowserBase):
    """
    Window Class
    """

    def __init__(
        self, *args, browser: Firefox, handle: str | None = None, **kwargs
    ) -> None:
        """
        Constructor

        Parameters
        ----------
        browser : Firefox
            Browser instance

        handle : str | None
            Window handle, by default None
        """

        super().__init__(*args, **kwargs)

        # Parameters
        self.browser: Firefox = browser
        self.handle: str | None = handle

    # pylint: disable=arguments-differ
    # Overriding method from BrowserBase
    def open(self, url: str) -> str:
        """
        Open new Window

        Parameters
        ----------
        url : str
            URL to open

        Returns
        -------
        str: Window Handle

        Notes
        -----
        This method will open a new window within the browser.
        It will save and return the window handle.
        """

        # Format url if provided. Set open blank page if not.
        url = self._format_url(url) if url else "about:blank"

        # Open new window
        self.browser.execute_script(f"window.open('{url}');")

        # Get window handle
        self.handle = self.browser.window_handles[-1]

        # Switch to new window
        self.browser.switch_to.window(self.handle)

        return self.handle

    # pylint: disable=arguments-differ
    # Overriding method from BrowserBase
    def close(self) -> None:
        """Close Window"""

        self.browser.close()
