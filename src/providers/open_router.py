from crewai import LLM
import os
from dotenv import load_dotenv
load_dotenv()
open_router_api_key = os.getenv("OPEN_ROUTER_API_KEY")

deepseek_v3 = LLM(
    model="openrouter/deepseek/deepseek-chat-v3-0324:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=open_router_api_key,
    temperature=0
)

mistral_small = LLM(
    model="openrouter/mistralai/mistral-small-3.1-24b-instruct:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=open_router_api_key,
    temperature=0
)