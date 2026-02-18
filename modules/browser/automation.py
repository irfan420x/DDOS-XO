# Path: modules/browser/automation.py

import webbrowser
from loguru import logger

class BrowserAutomation:
    def __init__(self, config):
        self.config = config

    def open_url(self, url: str):
        logger.info(f"Opening browser: {url}")
        try:
            webbrowser.open(url)
            return f"Opened {url} in your default browser."
        except Exception as e:
            return f"Failed to open browser: {str(e)}"

    def search(self, query: str):
        url = f"https://www.google.com/search?q={query}"
        return self.open_url(url)
