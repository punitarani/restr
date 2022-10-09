"""Browser test fixtures"""

import pytest

from restr.browser import Browser, Options

# Cache browser
__BROWSER = None


@pytest.fixture
def browser():
    """Create Browser fixture"""

    # pylint: disable=global-statement
    # Need to cache browser
    global __BROWSER

    # Create and cache browser
    if not __BROWSER or __BROWSER.browser.service.process is None:
        # Define Firefox Options
        options = Options()
        options.headless = True

        # Create browser and wait 3s to open
        __BROWSER = Browser(options=options)
        __BROWSER.browser.implicitly_wait(3)

    return __BROWSER


@pytest.fixture(scope="module", autouse=True)
def close_browser():
    """
    Close browser after all tests.
    Called automatically at the end of each module.
    """

    # Run tests
    yield

    # Close browser if it's still open after tests
    if isinstance(__BROWSER, Browser) and __BROWSER.browser.service.process:
        __BROWSER.close()
