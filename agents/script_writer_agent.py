"""
agents/script_writer_agent.py
Agent 3: Writes a 60-second video ad script based on marketing analysis + brand data.
"""
from crewai import Agent, Task
from tools.gdrive_fetcher import gdrive_fetcher_tool
from config.settings import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL


def build_script_writer_agent() -> Agent:
    return Agent(
        role="Video Ad Script Writer",
        goal=(
            "Write a powerful 60-second video ad script for CrowdWisdomTrading that "
            "leverages the winning pain points identified from competitor research, "
            "uses the brand's unique data and proof, and follows a proven "
            "hook → problem → solution → proof → CTA structure."
        ),
        backstory=(
            "You are an elite video ad scriptwriter who has written scripts for "
            "7-figure trading education brands. You understand that a great 60-second ad "
            "must grab attention in the first 3 seconds, build desire in seconds 10-45, "
            "and drive action with urgency in the final 15 seconds. "
            "You write for the ear, not the eye — short sentences, punchy language, "
            "and emotional resonance. You make every word earn its place."
        ),
        tools=[gdrive_fetcher_tool],
        llm=_llm_config(),
        verbose=True,
        allow_delegation=False,
        max_retry_limit=3,
    )


def build_script_task(agent: Agent, context_tasks: list) -> Task:
    return Task(
        description=(
            "Use the Google Drive Brand Data Fetcher tool to load CrowdWisdomTrading's "
            "brand and product data. Then, using the marketing intelligence from the "
            "previous agent, write a complete 60-second video ad script.\n\n"
            "SCRIPT REQUIREMENTS:\n"
            "- Total runtime: 55-65 seconds when read at natural pace\n"
            "- Hook (0-3s): Interrupt pattern that stops the scroll. Use the top pain point.\n"
            "- Problem Agitation (3-15s): Make the pain real and personal. Be specific.\n"
            "- Solution Reveal (15-30s): Introduce CrowdWisdomTrading as THE answer.\n"
            "- Proof/Benefits (30-45s): 3 specific results/benefits with social proof.\n"
            "- Urgency + CTA (45-60s): Clear action step with scarcity or urgency.\n\n"
            "TONE: Conversational, direct, urgent. Like a trusted friend giving advice.\n"
            "NO buzzwords. NO fluff. Every word serves a purpose.\n\n"
            "Also provide the Remotion scene breakdown as a JSON structure with "
            "fields: title, hook, scenes (each with text and duration_secs), cta, "
            "primary_color (#00C2FF), accent_color (#FFD700), bg_color (#0A0A1A).\n\n"
            "Call gdrive_fetcher_tool with an empty string to load brand data."
        ),
        expected_output=(
            "Two outputs:\n"
            "1. FULL_SCRIPT: The complete 60-second spoken script as plain text\n"
            "2. REMOTION_JSON: A JSON object with keys: title, hook (3s opener text), "
            "scenes (list of {text, duration_secs} for each scene section), "
            "cta (final CTA text), primary_color, accent_color, bg_color. "
            "Total scene duration_secs should sum to ~54 seconds."
        ),
        agent=agent,
        context=context_tasks,
    )


def _llm_config():
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=OPENROUTER_MODEL,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base=OPENROUTER_BASE_URL,
        temperature=0.7,
        max_tokens=6000,
        default_headers={
            "HTTP-Referer": "https://crowdwisdomtrading.com",
            "X-Title": "CWT Ads Agent",
        },
    )
