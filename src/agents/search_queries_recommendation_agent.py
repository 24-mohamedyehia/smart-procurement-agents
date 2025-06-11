import os
from crewai import Agent , Task
from src.providers import mistral_small
from src.models import SuggestedSearchQueries

output_dir = '/src/ai-agent-output'

search_queries_recommendation = Agent(
    role="Search Queries Recommendation Agent",
    goal="Produce ecommerce-style search queries that hit only product pages for any given product.",
    backstory="\n".join([
        "The agent is designed to help in looking for products by providing a list of suggested search queries to be passed to the search engine based on the context provided."
        "You need to generate queries that:",
        "provid the best suggested search queries with details"
        "- Restrict to specific sites: use site: keyword for search",
    ]),
    llm=mistral_small,
    verbose=True
)


search_queries_recommendation_task = Task(
    description="\n".join([
        "Our company is looking to buy {product_name} at the best prices (value-for-price).",
        "Targets these sites: {websites_list} in {country_name}.",
        "Generate up to {no_keywords} queries in {language}.",
        "Queries must:",
        "  • must be detail and add more description to find the best queries",
        "  • Use site: operator to restrict domain, e.g. site:{websites_list}",
        "  . The search keywords must be in {language} language."
        "  • Include specific features or model numbers if known (placeholders).",
    ]),
    expected_output="A JSON object containing a list of suggested search queries.",
    output_json=SuggestedSearchQueries,
    output_file=os.path.join(output_dir, "step_1_suggested_search_queries.json"),
    agent=search_queries_recommendation
)