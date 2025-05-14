import json
from crewai.tools import tool
from tavily import TavilyClient
from scrapegraph_py import Client
from src.models import SingleExtractedProduct
from dotenv import load_dotenv
import os
load_dotenv()

search_client = TavilyClient(api_key=os.getenv("TVLY_SEARCH_API_KEY"))
scrape_client = Client(api_key=os.getenv('Scrapegraph_API_KEY'))


@tool
def read_json(file_path: str):
    """
    Read a JSON file from the given file path and return its content as a dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@tool
def search_engine_tool(query: str):
    """
    Perform a search for the given query using the configured search client.
    Returns a dictionary containing search results with title, url, content, and score.
    """
    return search_client.search(query)

@tool
def web_scraping_tool(page_url: str):
    """
    Scrapes a single product page and returns the extracted details.
    """
    schema = SingleExtractedProduct.model_json_schema()
    details = scrape_client.smartscraper(
        website_url=page_url,
        user_prompt=f"Extract {json.dumps(schema, ensure_ascii=False)} from the page"
    )
    return {"page_url": page_url, "details": details}
