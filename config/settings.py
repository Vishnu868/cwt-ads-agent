"""
config/settings.py
Centralised settings loaded from .env
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── LLM ────────────────────────────────────────────────────
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL: str = os.getenv(
    "OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free"
)

# ─── APIFY ───────────────────────────────────────────────────
APIFY_API_TOKEN: str = os.getenv("APIFY_API_TOKEN", "")

# ─── ELEVENLABS ──────────────────────────────────────────────
ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

# ─── GOOGLE DRIVE ────────────────────────────────────────────
GOOGLE_CREDENTIALS_PATH: str = os.getenv(
    "GOOGLE_CREDENTIALS_PATH", "credentials/google_credentials.json"
)
GDRIVE_FILE_ID: str = os.getenv(
    "GDRIVE_FILE_ID", "1j5ElESYs4mkQQ-0laPy37ZPgvOLLHyVP"
)

# ─── OUTPUT ──────────────────────────────────────────────────
OUTPUT_DIR: Path = BASE_DIR / os.getenv("OUTPUT_DIR", "outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REMOTION_PROJECT_DIR: Path = BASE_DIR / os.getenv(
    "REMOTION_PROJECT_DIR", "remotion_project"
)

# ─── CAMPAIGN TARGET ────────────────────────────────────────
TARGET_BRAND: str = "CrowdWisdomTrading"
TARGET_WEBSITE: str = "crowdwisdomtrading.com"
TARGET_NICHE: str = "stock trading education"
NICHE_KEYWORDS: list[str] = [
    "stock trading",
    "trading signals",
    "trading community",
    "stock market",
    "trading education",
    "day trading",
    "swing trading",
    "trading alerts",
]
ADS_LOOKBACK_DAYS: int = 30
MAX_ADS_TO_ANALYSE: int = 20
