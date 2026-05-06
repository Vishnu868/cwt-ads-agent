"""
test_pipeline.py
Standalone test script to validate each component individually.
Run before the full pipeline to confirm all integrations work.

Usage:
    python test_pipeline.py              # Test all
    python test_pipeline.py --tool apify # Test only apify
    python test_pipeline.py --tool gdrive
    python test_pipeline.py --tool tts
    python test_pipeline.py --tool remotion
"""
import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from loguru import logger

console = Console()


def test_apify():
    """Test Apify Meta Ads scraper."""
    console.print("\n[bold cyan]Testing Apify Meta Ads Scraper...[/bold cyan]")
    try:
        from tools.apify_scraper import scrape_meta_ads, save_ads_to_json
        ads = scrape_meta_ads()
        path = save_ads_to_json(ads)
        console.print(f"[green]✓ Scraped {len(ads)} ads → {path}[/green]")
        if ads:
            console.print(f"  First ad preview: {json.dumps(ads[0], indent=2)[:400]}...")
        return True
    except Exception as e:
        console.print(f"[red]✗ Apify test failed: {e}[/red]")
        return False


def test_gdrive():
    """Test Google Drive fetcher."""
    console.print("\n[bold cyan]Testing Google Drive Fetcher...[/bold cyan]")
    try:
        from tools.gdrive_fetcher import fetch_gdrive_content
        content = fetch_gdrive_content()
        console.print(f"[green]✓ Fetched {len(content)} chars from GDrive[/green]")
        console.print(f"  Preview: {content[:200]}...")
        return True
    except Exception as e:
        console.print(f"[red]✗ GDrive test failed: {e}[/red]")
        return False


def test_tts():
    """Test ElevenLabs TTS."""
    console.print("\n[bold cyan]Testing ElevenLabs TTS...[/bold cyan]")
    try:
        from tools.elevenlabs_tts import generate_voiceover
        test_text = (
            "Are you tired of missing winning trades while others profit? "
            "Join 10,000 traders at CrowdWisdomTrading and get real-time signals today."
        )
        path = generate_voiceover(test_text, "test_voiceover.mp3")
        console.print(f"[green]✓ Voiceover generated → {path}[/green]")
        return True
    except Exception as e:
        console.print(f"[red]✗ ElevenLabs test failed: {e}[/red]")
        return False


def test_remotion():
    """Test Remotion project scaffolding."""
    console.print("\n[bold cyan]Testing Remotion Video Builder...[/bold cyan]")
    try:
        from tools.remotion_builder import write_remotion_project

        sample_script = {
            "title": "CWT Test Ad",
            "hook": "Are you losing money trading alone?",
            "scenes": [
                {"text": "Most traders lose because they have no edge", "duration_secs": 5},
                {"text": "CrowdWisdomTrading gives you real-time signals", "duration_secs": 5},
                {"text": "Join 10,000+ traders making consistent profits", "duration_secs": 5},
            ],
            "cta": "Join CrowdWisdomTrading FREE Today",
            "primary_color": "#00C2FF",
            "accent_color": "#FFD700",
            "bg_color": "#0A0A1A",
        }

        project_dir = write_remotion_project(sample_script)
        files = list(project_dir.rglob("*.jsx")) + list(project_dir.rglob("*.json"))
        console.print(f"[green]✓ Remotion project written → {project_dir}[/green]")
        for f in files:
            console.print(f"  {f.relative_to(project_dir)}")
        return True
    except Exception as e:
        console.print(f"[red]✗ Remotion test failed: {e}[/red]")
        return False


def run_all():
    results = {
        "apify": test_apify(),
        "gdrive": test_gdrive(),
        "tts": test_tts(),
        "remotion": test_remotion(),
    }

    table = Table(title="Test Results", style="bold")
    table.add_column("Component", style="bold white")
    table.add_column("Status")

    for name, passed in results.items():
        status = "[green]✓ PASS[/green]" if passed else "[red]✗ FAIL[/red]"
        table.add_row(name.upper(), status)

    console.print(table)
    all_pass = all(results.values())
    if all_pass:
        console.print("\n[bold green]All tests passed! Ready to run main.py[/bold green]")
    else:
        console.print("\n[bold yellow]Some tests failed. Check your .env file and API keys.[/bold yellow]")
    return all_pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", choices=["apify", "gdrive", "tts", "remotion", "all"],
                        default="all")
    args = parser.parse_args()

    tests = {
        "apify": test_apify,
        "gdrive": test_gdrive,
        "tts": test_tts,
        "remotion": test_remotion,
    }

    if args.tool == "all":
        success = run_all()
    else:
        success = tests[args.tool]()

    sys.exit(0 if success else 1)
