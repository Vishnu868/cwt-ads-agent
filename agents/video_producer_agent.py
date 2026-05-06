"""
agents/video_producer_agent.py
Agent 4: Produces the final 60-second video ad using ElevenLabs TTS + Remotion.
"""
import json
import re
from pathlib import Path

from crewai import Agent, Task
from loguru import logger

from tools.elevenlabs_tts import tts_tool
from tools.remotion_builder import remotion_builder_tool
from config.settings import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL, OUTPUT_DIR


def build_video_producer_agent() -> Agent:
    return Agent(
        role="Video Ad Producer",
        goal=(
            "Transform the ad script into a polished 60-second video ad with "
            "professional voiceover, animated text scenes, and dynamic subtitles "
            "using ElevenLabs for voice and Remotion for video rendering."
        ),
        backstory=(
            "You are a digital video producer specialising in performance marketing "
            "content. You know how to take a script and turn it into a video that "
            "gets results on Instagram Reels and Facebook Stories. "
            "You orchestrate audio generation and video rendering pipelines "
            "with precision, handling errors gracefully and always delivering output."
        ),
        tools=[tts_tool, remotion_builder_tool],
        llm=_llm_config(),
        verbose=True,
        allow_delegation=False,
        max_retry_limit=3,
    )


def build_video_task(agent: Agent, context_tasks: list) -> Task:
    return Task(
        description=(
            "Using the full ad script and Remotion JSON from the script writer agent:\n\n"
            "STEP 1 — VOICEOVER:\n"
            "Extract the full spoken script text from the previous agent's output "
            "and call the ElevenLabs TTS tool with it to generate professional voiceover audio.\n\n"
            "STEP 2 — VIDEO PRODUCTION:\n"
            "Take the REMOTION_JSON from the script writer and add the audio file path "
            "(from step 1) as 'audio_file' key. Then call the Remotion Video Builder tool "
            "with the complete JSON to render the final video.\n\n"
            "STEP 3 — REPORT:\n"
            "Provide a complete production summary including:\n"
            "- Path to the rendered video\n"
            "- Path to the voiceover audio\n"
            "- Script used\n"
            "- Total video duration\n"
            "- Next steps for publishing\n\n"
            "If ElevenLabs fails (e.g., no API key), note it and proceed with video "
            "production without audio — the structure will still be complete.\n"
            "If Remotion rendering fails, provide the render command and project directory "
            "so it can be run manually."
        ),
        expected_output=(
            "A production completion report with: "
            "video_path, audio_path, script_text, total_seconds, "
            "status (complete/partial), and next_steps list. "
            "Also include the full Remotion render command for manual use if needed."
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
        temperature=0.2,
        max_tokens=4000,
        default_headers={
            "HTTP-Referer": "https://crowdwisdomtrading.com",
            "X-Title": "CWT Ads Agent",
        },
    )
