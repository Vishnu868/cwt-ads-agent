"""
tools/elevenlabs_tts.py
Generates voiceover audio from text using ElevenLabs API.
"""
import json
from pathlib import Path

import requests
from loguru import logger

from config.settings import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, OUTPUT_DIR


ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def generate_voiceover(script_text: str, output_filename: str = "voiceover.mp3", **kwargs) -> Path:
    from gtts import gTTS
    output_path = OUTPUT_DIR / output_filename
    tts = gTTS(text=script_text, lang='en', slow=False)
    tts.save(str(output_path))
    logger.success(f"Voiceover saved → {output_path}")
    return output_path

def get_available_voices() -> list[dict]:
    """Fetch list of available voices from ElevenLabs."""
    resp = requests.get(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": ELEVENLABS_API_KEY},
        timeout=20,
    )
    if resp.status_code == 200:
        return resp.json().get("voices", [])
    return []