"""Browser automation for SlovioV2."""

import subprocess
import os
from typing import Optional, Tuple


class BrowserAgent:
    """Browser automation using ydotool + direct URL opening."""

    def __init__(self):
        self.browser = "firefox"

    def open_browser(self, url: str = "https://google.com") -> bool:
        """Open browser with URL."""
        try:
            subprocess.Popen([self.browser, url])
            return True
        except:
            try:
                subprocess.Popen(["chromium", url])
                return True
            except:
                return False

    def search_google(self, query: str) -> bool:
        """Open browser and search Google."""
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return self.open_browser(url)

    def open_url(self, url: str) -> bool:
        """Open a specific URL."""
        return self.open_browser(url)


# Singleton instance
_browser_agent = None


def get_browser_agent():
    global _browser_agent
    if _browser_agent is None:
        _browser_agent = BrowserAgent()
    return _browser_agent
