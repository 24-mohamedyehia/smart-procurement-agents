from src.models import AllExtractedProducts
from crewai import Agent, Task
import os
from src.providers import deepseek_v3
from src.tools import web_scraping_tool, read_json

output_dir = 'src/ai-agent-output'

scraper = Agent(
    role="Expert Web Scraping Agent",
    goal="Accurately extract key product details from e-commerce websites and format them into a structured JSON object.",
    backstory=(
        "You are a master web scraping agent. Your specialty is analyzing the HTML of any e-commerce product page "
        "to find specific information like price, title, specifications, and availability. "
        "You are highly resilient and know how to handle errors. If a URL is broken, times out, or is not a product page, "
        "you will log a note about the failure and move to the next URL without crashing."
    ),
    llm=deepseek_v3,
    tools=[web_scraping_tool, read_json],
    verbose=True,
    allow_delegation=False,
)


scraping_task = Task(
    description=(
        "1. You will be given a list of URLs in {search_results}. \n"
        "2. Your goal is to select the best {top_recommendations_no} products from this list. \n"
        "3. For each URL, visit the page and extract the product details required by the `SingleExtractedProduct` model. \n"
        "4. Pay close attention to extracting: Title, current price, currency (e.g., EGP), availability, and 1-5 key specifications. \n"
        "6. If you encounter a broken URL or a page that is not a product page, skip it and proceed to the next one. \n"
        "7. Compile all successfully extracted products into a final JSON object."
    ),
    expected_output="A final JSON object that strictly follows the `AllExtractedProducts` schema.",
    output_json=AllExtractedProducts,
    output_file=os.path.join(output_dir, "step_3_products_file.json"),
    agent=scraper
)