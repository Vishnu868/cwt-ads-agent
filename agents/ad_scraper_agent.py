"""
agents/ad_scraper_agent.py
Agent 1: Searches and selects the best performing Meta Ads in the CWT niche.
"""
from crewai import Agent, Task
from loguru import logger

from tools.apify_scraper import meta_ads_scraper_tool
from config.settings import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL


def build_scraper_agent() -> Agent:
    return Agent(
        role="Meta Ads Intelligence Specialist",
        goal=(
            "Discover and curate the top performing Meta (Facebook/Instagram) ads "
            "in the stock trading education niche, active in the last 30 days. "
            "Find ads that are getting traction, have strong hooks, and compelling offers."
        ),
        backstory=(
            "You are an expert digital marketing researcher with 8 years of experience "
            "analysing Meta Ads for high-converting funnels. You have an eye for what "
            "makes trading education ads work: the hook, the pain point, the promise, "
            "and the proof. You use the Meta Ads Library to find what's actually working "
            "right now, not theory."
        ),
        tools=[meta_ads_scraper_tool],
        llm=_llm_config(),
        verbose=True,
        allow_delegation=False,
        max_retry_limit=3,
    )


def build_scraper_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Use the Meta Ads Scraper tool to search for ads related to "
            "CrowdWisdomTrading's niche (stock trading education, trading signals, "
            "trading community, day trading). "
            "\n\nYour job:\n"
            "1. Run the scraper tool with an empty query string to trigger it\n"
            "2. Review the returned ads data\n"
            "3. Identify the TOP 10 ads based on: recency, engagement signals, "
            "strong hook language, and clear pain-point targeting\n"
            "4. Return a structured summary of the best 10 ads with: "
            "ad_text, headline, page_name, why_it_works (your analysis), and "
            "key_message\n\n"
            "The scraper saves results to a JSON file automatically."
        ),
        expected_output=(
            "A JSON array of the top 10 ads, each with: "
            "id, page_name, ad_text, headline, cta, why_it_works (2-3 sentences), "
            "and key_message. Also include a brief summary of common themes across ads."
        ),
        agent=agent,
    )


def _llm_config():
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=OPENROUTER_MODEL,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base=OPENROUTER_BASE_URL,
        temperature=0.3,
        max_tokens=4000,
        default_headers={
            "HTTP-Referer": "https://crowdwisdomtrading.com",
            "X-Title": "CWT Ads Agent",
        },
    )
