import json
from crewai.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os
load_dotenv()

search_client = TavilyClient(api_key=os.getenv("TVLY_SEARCH_API_KEY"))


@tool
def read_json(file_path: str):
    """
    Read a JSON file from the given file path and return its content as a dictionary.
    Tries to handle encoding errors gracefully.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin1') as f:
            return json.load(f)

@tool
def search_engine_tool(query: str):
    """
    Perform a search for the given query using the configured search client.
    Returns a dictionary containing search results with title, url, content, and score.
    """
    return search_client.search(query)
