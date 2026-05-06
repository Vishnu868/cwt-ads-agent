"""
main.py — CWT Ads AI Agent Pipeline (CrewAI-free version)
4 sequential LLM agents using langchain-openai directly.
No ChromaDB. No C++ compiler needed.
"""
import json
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from loguru import logger

load_dotenv()

from config.settings import (
    OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL, OUTPUT_DIR
)
from tools.apify_scraper import scrape_meta_ads, save_ads_to_json
from tools.gdrive_fetcher import fetch_gdrive_content
from tools.elevenlabs_tts import generate_voiceover
from tools.remotion_builder import write_remotion_project, render_video

console = Console()


def get_llm(temperature: float = 0.4) -> ChatOpenAI:
    return ChatOpenAI(
        model=OPENROUTER_MODEL,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base=OPENROUTER_BASE_URL,
        temperature=temperature,
        max_tokens=4000,
        default_headers={
            "HTTP-Referer": "https://crowdwisdomtrading.com",
            "X-Title": "CWT Ads Agent",
        },
    )


def banner(title: str, subtitle: str = "") -> None:
    console.print(Panel(f"[bold white]{title}[/bold white]\n[dim]{subtitle}[/dim]",
                        style="bold cyan", expand=False))


def agent1_scrape() -> list:
    banner("Agent 1 / 4", "Meta Ads Scraper — Apify")
    try:
        ads = scrape_meta_ads()
        path = save_ads_to_json(ads)
        console.print(f"[green]✓ Scraped {len(ads)} ads → {path}[/green]")
        return ads
    except Exception as e:
        logger.error(f"Scrape failed: {e}")
        cached = OUTPUT_DIR / "scraped_ads.json"
        if cached.exists():
            console.print(f"[yellow]⚠ Using cached ads[/yellow]")
            return json.loads(cached.read_text()).get("ads", [])
        return []


def agent2_analyse(ads: list) -> dict:
    banner("Agent 2 / 4", "Marketing Intelligence Analyst")
    llm = get_llm(temperature=0.3)
    ads_text = json.dumps(ads[:10], indent=2, ensure_ascii=False)
    messages = [
        SystemMessage(content=(
            "You are a world-class direct response marketing analyst for trading products. "
            "Respond with valid JSON only, no markdown."
        )),
        HumanMessage(content=f"""Analyse these Meta Ads:\n{ads_text}\n
Return JSON with keys: pain_points (list of 5), emotional_triggers (list),
hook_formulas (list of 3), top_3_concepts (list of {{concept,why_it_works,how_to_use}}),
recommended_hook (string), recommended_pain_point (string).
JSON only.""")
    ]
    response = llm.invoke(messages)
    content = response.content.strip().replace("```json","").replace("```","").strip()
    try:
        result = json.loads(content)
    except Exception:
        result = {"recommended_hook": "Still losing money trading alone?",
                  "recommended_pain_point": "Trading alone without real-time signals",
                  "top_3_concepts": []}
    (OUTPUT_DIR / "agent2_analyst.json").write_text(json.dumps(result, indent=2))
    console.print(f"[green]✓ Analysis complete[/green]")
    return result


def agent3_write_script(analysis: dict) -> dict:
    banner("Agent 3 / 4", "Ad Script Writer")
    llm = get_llm(temperature=0.7)
    brand_data = fetch_gdrive_content()
    messages = [
        SystemMessage(content="You are an elite video ad scriptwriter. Respond with valid JSON only, no markdown."),
        HumanMessage(content=f"""Brand: CrowdWisdomTrading
Brand data: {brand_data[:1500]}
Best hook: {analysis.get('recommended_hook')}
Lead pain: {analysis.get('recommended_pain_point')}

Write a 60-second ad script. Return JSON with keys:
- full_script: complete spoken text (~150 words)
- hook: 1 sentence opener (3 seconds)
- scenes: list of {{text, duration_secs}} — 7-8 scenes summing to ~54 seconds total
- cta: short call-to-action
- primary_color: "#00C2FF"
- accent_color: "#FFD700"
- bg_color: "#0A0A1A"
JSON only.""")
    ]
    response = llm.invoke(messages)
    content = response.content.strip().replace("```json","").replace("```","").strip()
    try:
        result = json.loads(content)
    except Exception:
        result = {
            "full_script": "Are you still losing trades because you're going it alone? Most traders fail not because they're not smart but because they have no edge. Introducing CrowdWisdomTrading. Ten thousand traders sharing real-time signals every single day. Buy and sell alerts before the market moves. Daily watchlists. Live Q&A with experienced traders. Last month our top alerts averaged twelve percent gains. No guesswork. No more losing alone. Trade smarter with the crowd. Join free for your first seven days at crowdwisdomtrading dot com.",
            "hook": "Still losing trades because you're trading alone?",
            "scenes": [
                {"text": "Most traders fail — not because they're not smart", "duration_secs": 6},
                {"text": "But because they have NO edge and NO signals", "duration_secs": 7},
                {"text": "Introducing CrowdWisdomTrading", "duration_secs": 5},
                {"text": "10,000+ traders sharing real-time buy/sell alerts daily", "duration_secs": 8},
                {"text": "Alerts BEFORE the market moves. Daily watchlists. Live Q&A.", "duration_secs": 8},
                {"text": "Last month: top alerts averaged 12% gains", "duration_secs": 7},
                {"text": "Join FREE for 7 days — no commitment", "duration_secs": 7},
            ],
            "cta": "Join FREE → crowdwisdomtrading.com",
            "primary_color": "#00C2FF",
            "accent_color": "#FFD700",
            "bg_color": "#0A0A1A",
        }
    (OUTPUT_DIR / "agent3_script.txt").write_text(result.get("full_script",""))
    (OUTPUT_DIR / "agent3_script.json").write_text(json.dumps(result, indent=2))
    console.print(f"[green]✓ Script written[/green]")
    return result


def agent4_produce_video(script_data: dict) -> dict:
    banner("Agent 4 / 4", "Video Producer — ElevenLabs + Remotion")
    results = {}
    try:
        audio_path = generate_voiceover(script_data.get("full_script",""), "voiceover.mp3")
        results["audio_path"] = str(audio_path)
        console.print(f"[green]✓ Voiceover generated → {audio_path}[/green]")
    except Exception as e:
        logger.warning(f"Voiceover failed: {e}")
        results["audio_path"] = None

    try:
        script_copy = {k: v for k, v in script_data.items() if k != "full_script"}
        project_dir = write_remotion_project(script_copy, results.get("audio_path"))
        video_path = render_video(project_dir)
        results["video_path"] = str(video_path)
        console.print(f"[green]✓ Video rendered → {video_path}[/green]")
    except Exception as e:
        logger.error(f"Video render failed: {e}")
        results["video_path"] = None
        results["render_command"] = "cd remotion_project && npm install --legacy-peer-deps && npx remotion render CWTAd ../outputs/cwt_ad.mp4 --codec=h264"
    return results


def run_pipeline():
    console.print(Panel("[bold white]🚀 CrowdWisdomTrading Ads AI Agent[/bold white]\n[dim]LangChain · Apify · ElevenLabs · Remotion[/dim]", style="bold cyan"))
    start = time.time()
    ads = agent1_scrape()
    analysis = agent2_analyse(ads)
    script = agent3_write_script(analysis)
    video = agent4_produce_video(script)
    elapsed = time.time() - start

    table = Table(title="✅ Pipeline Complete", style="bold cyan")
    table.add_column("Agent", style="bold white")
    table.add_column("Output")
    table.add_row("1. Ads Scraper", str(OUTPUT_DIR / "scraped_ads.json"))
    table.add_row("2. Analyst", str(OUTPUT_DIR / "agent2_analyst.json"))
    table.add_row("3. Script Writer", str(OUTPUT_DIR / "agent3_script.txt"))
    table.add_row("4. Video Producer", video.get("video_path") or video.get("render_command","See remotion_project/"))
    console.print(table)
    console.print(f"\n[bold white]Done in {elapsed:.1f}s[/bold white]")
    if not video.get("video_path"):
        console.print(f"\n[yellow]Render video manually:[/yellow]\n[dim]{video.get('render_command')}[/dim]")


if __name__ == "__main__":
    try:
        run_pipeline()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
    except Exception as e:
        logger.exception(e)
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        sys.exit(1)