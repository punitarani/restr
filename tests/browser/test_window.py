"""tests.browser.window"""

from selenium.webdriver.support import expected_conditions, wait

from restr.browser.window import Window


class TestWindow:
    """Test Window"""

    def test_init(self, browser):
        """Test Init"""

        window = Window(browser=browser.browser)
        assert window.browser == browser.browser
        assert window.handle is None

    def test_open(self, browser):
        """Test Open"""

        window = browser.windows[browser.browser.current_window_handle]

        # Open window
        window.open("https://www.icann.org/")

        # Verify window is open and has the current window handle
        assert window.handle in browser.browser.window_handles
        assert window.handle == browser.browser.current_window_handle

        # Wait for page to load. Title should be something
        wait.WebDriverWait(browser.browser, 10).until(
            expected_conditions.title_is("Homepage")
        )

        # Verify window url is correct
        assert window.browser.current_url == "https://www.icann.org/"

    def test_close(self, browser):
        """Test Close"""

        window = Window(browser=browser.browser)
        window.open("https://www.icann.org/")

        # Close window
        window.close()

        # Verify window is closed
        assert window.handle not in browser.windows

        # Verify browser is still open
        assert browser.browser.service.process is not None

        # Close browser
        browser.close()
