from src.agents import search_queries_recommendation, search_queries_recommendation_task
from src.agents import search_engine, search_engine_task
from src.agents import scraper, scraping_task
from src.agents import procurement_report, procurement_report_task
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import agentops
from crewai import Crew, Process
import os
from dotenv import load_dotenv

load_dotenv()
agentops_api_key = os.getenv("Agentops_API_KEY")

agentops.init(
    api_key=agentops_api_key,
    skip_auto_end_session=True
)

company_context = StringKnowledgeSource(
    content="""
            TestAI is a company that provides AI solutions to help websites refine their search and recommendation systems.
            """
)

procurement_crew = Crew(
    agents=[
        search_queries_recommendation,
        search_engine,
        scraper,
        procurement_report
    ],
    tasks=[
        search_queries_recommendation_task,
        search_engine_task,
        scraping_task,
        procurement_report_task
    ],  
    process=Process.sequential,
    knowledge_sources=[company_context],
    verbose=True,
)