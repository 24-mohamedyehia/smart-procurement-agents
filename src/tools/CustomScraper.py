import time
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from crewai.tools import tool

# Model for raw and cleaned page content
each_page_content_schema = {
    "url": "string",
    "raw_html": "string",
    "clean_text": "string"
}

class PageContent(BaseModel):
    url: str
    clean_text: str

class GenericScraper:
    """
    A simple scraper that downloads full page content and returns it.
    """
    def __init__(self, wait_time: float = 1.0):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        self.wait_time = wait_time

    def fetch(self, url: str) -> str:
        time.sleep(self.wait_time)
        response = self.session.get(url, timeout=15)
        response.raise_for_status()
        return response.text

    def clean_text(self, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup(['script', 'style']):
            tag.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split())

    def scrape(self, url: str) -> PageContent:
        html = self.fetch(url)
        text = self.clean_text(html)
        return PageContent(url=url, clean_text=text)

# instantiate one scraper
generic_scraper = GenericScraper()

@tool
def web_scraping_tool(page_url: str):
    """
    Scrapes a single product page and returns the extracted details as a dictionary.
    Args:
        page_url (str): The URL of the product page to scrape.
    """
    # Fetch and clean page content
    page_content = generic_scraper.scrape(page_url)

    return {
        "page_content": page_content
    }

