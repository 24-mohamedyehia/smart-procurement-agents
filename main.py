from src.agents import search_queries_recommendation, search_queries_recommendation_task
from src.agents import search_engine, search_engine_task
from src.agents import scraper, scraping_task
from src.agents import procurement_report, procurement_report_task
from src.utils import clean_report
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import agentops
from crewai import Crew, Process
import os
import time
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

no_keywords = 3

output_dir = './src/ai-agent-output'
os.makedirs(output_dir, exist_ok=True)


procurement_crew = Crew(
    agents=[
        # search_queries_recommendation,
        # search_engine,
        # scraper,
        procurement_report
    ],
    tasks=[
        # search_queries_recommendation_task,
        # search_engine_task,
        # scraping_task,
        procurement_report_task
    ],  
    process=Process.sequential,
    knowledge_sources=[company_context],
    verbose=True,
)

crew_results = procurement_crew.kickoff(
    inputs={
        'product_name': 'labtop HP Gameing',
        'websites_list': ['www.amazon.eg', 'www.jumia.com.eg', 'www.noon.com/egypt-en'],
        'country_name': 'Egypt',
        'no_keywords': no_keywords,
        'language': 'English',
        'score_th': 0.5,
        'search_results': os.path.join(output_dir, 'step_2_search_results.json'),
        'top_recommendations_no': 2,
        'products_file': os.path.join(output_dir, 'step_3_products_file.json')
    }
)

time.sleep(3.0)  # Wait for the report to be generated

clean_report(os.path.join(output_dir, "step_4_procurement_report.html"))
