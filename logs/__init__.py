"""
Centralised logging configuration using loguru + rich.
"""
import sys
from pathlib import Path
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

# Remove default loguru handler
logger.remove()

# Pretty console output
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="DEBUG",
)

# File logging
log_path = Path("logs/pipeline.log")
log_path.parent.mkdir(parents=True, exist_ok=True)
logger.add(
    log_path,
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)


def banner(title: str, subtitle: str = "") -> None:
    """Print a rich banner for pipeline step."""
    text = Text(title, style="bold white")
    if subtitle:
        text.append(f"\n{subtitle}", style="dim white")
    console.print(Panel(text, style="bold cyan", expand=False))


def success(msg: str) -> None:
    console.print(f"[bold green]✓[/bold green] {msg}")


def warn(msg: str) -> None:
    console.print(f"[bold yellow]⚠[/bold yellow] {msg}")


def error(msg: str) -> None:
    console.print(f"[bold red]✗[/bold red] {msg}")
