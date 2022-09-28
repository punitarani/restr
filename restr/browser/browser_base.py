"""
restr.browser.browser_base.py

BrowserBase Class File
"""

from abc import ABC


class BrowserBase(ABC):
    """Browser Abstract Base Class"""

    def __init__(self, *args, **kwargs) -> None:
        """Constructor"""
        super().__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        """Open"""
        raise NotImplementedError

    def close(self, *args, **kwargs):
        """Close"""
        raise NotImplementedError

    @staticmethod
    def _format_url(url: str) -> str:
        """
        Format URL
        If URL does not start with http:// or https://, then https:// will be added.

        Parameters
        ----------
        url : str
            URL to format

        Returns
        -------
        str : Formatted URL

        Notes
        -----
        This is a protected method.
        """

        if not url.startswith("http"):
            url = f"https://{url}"

        return url
