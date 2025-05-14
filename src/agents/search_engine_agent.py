import os
from crewai import Agent , Task
from src.providers import ollama_llm
from src.models import AllSearchResults
from src.tools import search_engine_tool 


output_dir = '/src/ai-agent-output'

search_engine = Agent(
    role="Search Engine Agent",
    goal="To search for products based on the suggested search query",
    backstory=(
        "The agent is designed to help in looking for products by searching for products based on the suggested search queries."
    ),
    llm=ollama_llm, 
    tools=[search_engine_tool],
    verbose=True
)

search_engine_task = Task(
    description="""
    1. The task is to search for products based on suggested queries.
    2. You have to collect results from multiple search queries.
    3. Ignore any susbicious links or not an ecommerce single product website link.
    4. Ignore any search results with confidence score less than ({score_th}) .
    5. The search results will be used to compare prices of products from different websites.
    """,    
    expected_output="A JSON object conforming to the AllSearchResults model.",
    output_json=AllSearchResults,
    output_file=os.path.join(output_dir, "step_2_search_results.json"),
    agent=search_engine
)