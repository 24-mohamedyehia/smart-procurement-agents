from src.models import AllExtractedProducts
from crewai import Agent, Task
import os
from src.providers import ollama_llm
from src.tools import read_json, web_scraping_tool

output_dir = 'src/ai-agent-output'

scraper = Agent(
    role="Web Scraping Agent",
    goal="Extract and rank the best products from filtered URLs.",
    backstory="Loops over product URLs from  search_results json file, scrapes page details, and outputs the final JSON.",
    llm=ollama_llm,
    tools=[web_scraping_tool,read_json],
    verbose=True,
)

scraping_task = Task(
    description="\n".join([
        "Read {search_results}, loop over each URL in this file",
        "you can use  read_json tool to read all search_results",   
        "scrape details with web_scraping_tool,",
        "collect exactly {top_recommendations_no} products into a clean JSON."
    ]),
    expected_output="A JSON object containing products details",
    output_json=AllExtractedProducts,
    output_file=os.path.join(output_dir, "step_3_products_file.json"),
    agent=scraper
)
