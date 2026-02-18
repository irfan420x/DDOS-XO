# Path: automation/browser_controller.py
import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, Any, List

class BrowserController:
    """
    LUNA-ULTRA Browser Controller: Real web awareness using requests and BeautifulSoup.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def search(self, query: str) -> List[Dict[str, str]]:
        """
        Performs a Google search and returns titles and snippets.
        """
        logging.info(f"BrowserController: Searching for '{query}'")
        url = f"https://www.google.com/search?q={query}"
        try:
            import asyncio
            response = await asyncio.to_thread(requests.get, url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                for g in soup.find_all('div', class_='tF2Cxc'):
                    title = g.find('h3').text if g.find('h3') else ""
                    link = g.find('a')['href'] if g.find('a') else ""
                    snippet = g.find('div', class_='VwiC3b').text if g.find('div', class_='VwiC3b') else ""
                    if title and link:
                        results.append({"title": title, "link": link, "snippet": snippet})
                return results[:5]
            return []
        except Exception as e:
            logging.error(f"BrowserController Search Error: {e}")
            return []

    async def get_page_content(self, url: str) -> str:
        """
        Fetches and cleans the text content of a webpage.
        """
        logging.info(f"BrowserController: Fetching content from {url}")
        try:
            import asyncio
            response = await asyncio.to_thread(requests.get, url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text()
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                return text[:2000] # Limit to 2000 chars for LLM context
            return f"Error: Status code {response.status_code}"
        except Exception as e:
            logging.error(f"BrowserController Fetch Error: {e}")
            return str(e)
