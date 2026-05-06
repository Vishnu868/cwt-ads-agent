"""
agents/marketing_analyst_agent.py
Agent 2: Extracts marketing angles, pain points, and persuasion concepts from winning ads.
"""
from crewai import Agent, Task
from config.settings import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL


def build_analyst_agent() -> Agent:
    return Agent(
        role="Direct Response Marketing Analyst",
        goal=(
            "Extract deep marketing intelligence from winning ads: identify the exact "
            "pain points being targeted, the emotional triggers used, the unique selling "
            "propositions, and the persuasion frameworks that make these ads convert."
        ),
        backstory=(
            "You are a world-class direct response copywriter and marketing strategist "
            "who has studied over 50,000 high-converting ads. You understand buyer "
            "psychology, emotional triggers, and the 'job to be done' framework deeply. "
            "You can dissect any ad and identify exactly why it works or fails. "
            "You specialise in financial education and trading products."
        ),
        tools=[],
        llm=_llm_config(),
        verbose=True,
        allow_delegation=False,
        max_retry_limit=3,
    )


def build_analyst_task(agent: Agent, context_tasks: list) -> Task:
    return Task(
        description=(
            "Analyse the top performing Meta Ads provided by the previous agent. "
            "Perform deep marketing analysis to extract:\n\n"
            "1. **Pain Points** — What specific frustrations/fears are these ads targeting? "
            "(e.g., 'losing money trading alone', 'missing big moves', 'information overload')\n\n"
            "2. **Emotional Triggers** — What emotions are activated? "
            "(fear, greed, FOMO, shame, hope, envy, pride)\n\n"
            "3. **Hook Formulas** — What hook structures are working? "
            "(e.g., 'If you're a trader who [problem]...', 'Most traders don't know...')\n\n"
            "4. **Unique Angles** — What unique positioning or angles stand out?\n\n"
            "5. **Social Proof Patterns** — What types of proof are used?\n\n"
            "6. **CTA Patterns** — What calls to action convert best in this niche?\n\n"
            "7. **Top 3 Winning Concepts** — Summarise the 3 best marketing concepts "
            "that CrowdWisdomTrading should replicate/improve upon\n\n"
            "Format everything as structured JSON for use by the script writer."
        ),
        expected_output=(
            "A comprehensive marketing intelligence report as JSON with keys: "
            "pain_points (list), emotional_triggers (list), hook_formulas (list with examples), "
            "unique_angles (list), social_proof_patterns (list), cta_patterns (list), "
            "top_3_concepts (list of {concept, why_it_works, how_to_use}), "
            "recommended_primary_pain_point (string), recommended_hook (string)."
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
        temperature=0.4,
        max_tokens=4000,
        default_headers={
            "HTTP-Referer": "https://crowdwisdomtrading.com",
            "X-Title": "CWT Ads Agent",
        },
    )
