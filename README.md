# CrowdWisdomTrading — Ads AI Agent Pipeline

> **Intern Assessment Project** | Python · CrewAI · Apify · OpenRouter · ElevenLabs · Remotion

An end-to-end AI agent pipeline that automatically researches competitor ads, extracts marketing intelligence, writes a 60-second video ad script, generates a professional voiceover, and renders a full video — all from a single command.

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CrewAI Pipeline (Sequential)                  │
│                                                                   │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  │   Agent 1    │──▶│   Agent 2    │──▶│   Agent 3    │──▶│   Agent 4    │
│  │ Ads Scraper  │   │  Marketing   │   │   Script     │   │   Video      │
│  │              │   │  Analyst     │   │   Writer     │   │  Producer    │
│  │ Apify Meta   │   │              │   │ GDrive Data  │   │ ElevenLabs   │
│  │ Ads Library  │   │ Pain Points  │   │ 60s Script   │   │ + Remotion   │
│  │              │   │ Hook Angles  │   │ + JSON Plan  │   │   Render     │
│  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
│                                                                   │
│  Outputs:  scraped_ads.json  →  agent2_analyst.json  →  agent3_script.txt  →  cwt_ad.mp4
└─────────────────────────────────────────────────────────────────┘
```

### Agent Breakdown

| Agent | Role | Tools | Output |
|-------|------|-------|--------|
| **1. Ads Scraper** | Searches Meta Ads Library for CWT niche | Apify Meta Ads Library | `scraped_ads.json` |
| **2. Marketing Analyst** | Extracts pain points, hooks, persuasion patterns | LLM analysis | `agent2_analyst.json` |
| **3. Script Writer** | Writes 60s ad script using brand data + research | Google Drive fetcher | `agent3_script.txt` |
| **4. Video Producer** | Generates voiceover + renders Remotion video | ElevenLabs TTS, Remotion | `cwt_ad.mp4` |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/Vishnu868/cwt-ads-agent.git
cd cwt-ads-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Node.js (required for Remotion)
# Download from https://nodejs.org (v18+)
```

### 2. Configure API Keys

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

Required keys:
- `OPENROUTER_API_KEY` — [openrouter.ai](https://openrouter.ai) (free models available)
- `APIFY_API_TOKEN` — [apify.com](https://apify.com) (free tier)
- `ELEVENLABS_API_KEY` — [elevenlabs.io](https://elevenlabs.io) (free tier: 10k chars/month)

Optional:
- `GOOGLE_CREDENTIALS_PATH` — For fetching private GDrive files (falls back to embedded brand context if not set)
- `GDRIVE_FILE_ID` — Specific GDrive file to use as brand data source

### 3. Test Your Setup

```bash
python test_pipeline.py            # Test all integrations
python test_pipeline.py --tool apify   # Test only Apify
python test_pipeline.py --tool tts    # Test only ElevenLabs
```

### 4. Run the Pipeline

```bash
# Full pipeline (all 4 agents)
python main.py

# Skip ad scraping (use cached results)
python main.py --skip-scrape

# Only scrape + analyse (no video)
python main.py --script-only

# Only scrape ads
python main.py --scrape-only
```

---

## 📂 Project Structure

```
cwt-ads-agent/
├── main.py                    # Pipeline entry point
├── test_pipeline.py           # Individual tool testing
├── requirements.txt
├── .env.example
│
├── config/
│   ├── __init__.py
│   └── settings.py            # All settings from .env
│
├── agents/
│   ├── __init__.py
│   ├── ad_scraper_agent.py    # Agent 1
│   ├── marketing_analyst_agent.py  # Agent 2
│   ├── script_writer_agent.py     # Agent 3
│   └── video_producer_agent.py    # Agent 4
│
├── tools/
│   ├── __init__.py
│   ├── apify_scraper.py       # Apify Meta Ads Library integration
│   ├── gdrive_fetcher.py      # Google Drive brand data fetcher
│   ├── elevenlabs_tts.py      # ElevenLabs voiceover generation
│   └── remotion_builder.py   # Remotion video project builder
│
├── remotion_project/          # Auto-generated Remotion React project
│   ├── package.json
│   └── src/
│       ├── index.jsx          # Remotion root
│       ├── Root.jsx           # Main composition
│       ├── VideoComponent.jsx # Scene renderer
│       └── SubtitleComponent.jsx # Subtitle overlay
│
├── outputs/                   # All generated files
│   ├── scraped_ads.json
│   ├── agent2_analyst.json
│   ├── agent3_script.txt
│   ├── voiceover.mp3
│   └── cwt_ad.mp4
│
└── logs/
    └── pipeline.log
```

---

## 🎬 Video Output Specs

| Property | Value |
|----------|-------|
| Format | MP4 (H.264) |
| Resolution | 1080×1920 (9:16 vertical, Instagram/TikTok) |
| FPS | 30 |
| Duration | ~60 seconds |
| Audio | ElevenLabs AI voice (Rachel) |
| Subtitles | Dynamic word-by-word overlay |

### Video Structure

| Segment | Duration | Content |
|---------|----------|---------|
| Hook | 0–3s | Scroll-stopping pain point with glow effect |
| Problem Agitation | 3–15s | 2–3 scenes with trading frustrations |
| Solution Reveal | 15–30s | CrowdWisdomTrading introduction |
| Proof + Benefits | 30–45s | 3 specific results, social proof |
| CTA | 45–60s | Action prompt with pulse animation |

---

## 🔑 Getting API Keys

### Apify (Required — Free Tier)
1. Go to [apify.com](https://apify.com) → Sign up free
2. Dashboard → Settings → API & Integrations → Copy your API token
3. Free tier includes $5/month in usage (enough for ~100 ad scrapes)

### OpenRouter (Required — Free Models)
1. Go to [openrouter.ai](https://openrouter.ai) → Sign up
2. API Keys → Create new key
3. Recommended free model: `meta-llama/llama-3.3-70b-instruct:free`

### ElevenLabs (Optional — Free Tier)
1. Go to [elevenlabs.io](https://elevenlabs.io) → Sign up free
2. Profile → API Key → Copy
3. Free tier: 10,000 characters/month (~8 minutes of audio)

### Google Drive (Optional)
To fetch private GDrive files, create a service account:
1. [Google Cloud Console](https://console.cloud.google.com) → New project
2. Enable Drive API
3. Create service account → Download JSON key
4. Save as `credentials/google_credentials.json`
5. Share your GDrive file with the service account email

> **Note:** If GDrive credentials are not configured, the system automatically uses embedded CWT brand context. The pipeline works without Google credentials.

---

## 🎯 Customisation

### Change the Target Niche
Edit `config/settings.py`:
```python
TARGET_BRAND = "YourBrand"
TARGET_WEBSITE = "yourbrand.com"
NICHE_KEYWORDS = ["keyword1", "keyword2", ...]
```

### Change the AI Voice
In `.env`:
```
ELEVENLABS_VOICE_ID=your_voice_id_here
```
Get voice IDs from ElevenLabs dashboard or `tools/elevenlabs_tts.py::get_available_voices()`

### Change the LLM
In `.env`:
```
OPENROUTER_MODEL=anthropic/claude-3.5-haiku  # or any OpenRouter model
```

### Render Remotion Manually
If the auto-render fails (Node.js not installed), render manually:
```bash
cd remotion_project
npm install --legacy-peer-deps
npx remotion render CWTAd ../outputs/cwt_ad.mp4 --codec=h264
```

---

## 📊 Scaling

To scale the pipeline for multiple campaigns or daily runs:

```python
# Run for multiple niches
from main import run_full_pipeline
from config import settings

niches = ["stock trading", "crypto", "forex"]
for niche in niches:
    settings.TARGET_NICHE = niche
    run_full_pipeline(args)
```

**Scheduling (cron)**:
```bash
# Run daily at 9am
0 9 * * * cd /path/to/cwt-ads-agent && python main.py --skip-scrape >> logs/cron.log 2>&1
```

---

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| `Apify run failed` | Check APIFY_API_TOKEN, verify actor IDs are available in your region |
| `ElevenLabs TTS failed 401` | Check ELEVENLABS_API_KEY |
| `Remotion render failed` | Ensure Node.js 18+ is installed: `node --version` |
| `GDrive access denied` | Share the file with your service account email, or leave GOOGLE_CREDENTIALS_PATH empty to use fallback |
| `OpenRouter rate limit` | Switch to a different free model in .env |
| `Module not found` | Run `pip install -r requirements.txt` in your venv |

---

## 📝 Submission Notes

- **APIFY_API_TOKEN**: Will be included in email submission as required
- **Video Output**: See `outputs/` folder — rendered MP4 + sample frames
- **AI Tools Used**: Claude (Cursor-style), structure designed with Kiro patterns

---

## 📄 License

Built for CrowdWisdomTrading internship assessment. All API usage is within free-tier limits.
