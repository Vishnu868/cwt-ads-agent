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

Built for CrowdWisdomTrading internship assessment. All API usage is within free-tier limits.
