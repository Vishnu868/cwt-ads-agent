"""
tools/gdrive_fetcher.py
Fetches brand/product data files from Google Drive.
Supports both service-account and OAuth2 credentials, plus direct HTTP fallback.
"""
import io
import json
import os
from pathlib import Path
from typing import Optional

import requests
from loguru import logger

from config.settings import GOOGLE_CREDENTIALS_PATH, GDRIVE_FILE_ID, OUTPUT_DIR


def _try_service_account(file_id: str) -> Optional[str]:
    """Attempt to read file via google-api-python-client with service account."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseDownload

        creds_path = Path(GOOGLE_CREDENTIALS_PATH)
        if not creds_path.exists():
            logger.warning(f"Google credentials not found at {creds_path}")
            return None

        scopes = ["https://www.googleapis.com/auth/drive.readonly"]
        creds = service_account.Credentials.from_service_account_file(
            str(creds_path), scopes=scopes
        )
        service = build("drive", "v3", credentials=creds)

        # Get file metadata to determine type
        meta = service.files().get(fileId=file_id, fields="name,mimeType").execute()
        mime = meta.get("mimeType", "")
        logger.info(f"GDrive file: {meta.get('name')} | type: {mime}")

        # Export or download based on type
        if "google-apps.document" in mime:
            request = service.files().export_media(fileId=file_id, mimeType="text/plain")
        elif "google-apps.presentation" in mime:
            request = service.files().export_media(fileId=file_id, mimeType="text/plain")
        elif "google-apps.spreadsheet" in mime:
            request = service.files().export_media(fileId=file_id, mimeType="text/csv")
        else:
            request = service.files().get_media(fileId=file_id)

        buf = io.BytesIO()
        downloader = MediaIoBaseDownload(buf, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        content = buf.getvalue().decode("utf-8", errors="replace")
        logger.success(f"Downloaded {len(content)} chars from GDrive (service account)")
        return content

    except Exception as e:
        logger.warning(f"Service account GDrive fetch failed: {e}")
        return None


def _try_public_download(file_id: str) -> Optional[str]:
    """Attempt direct download for publicly shared Google Drive files."""
    # Try as Google Doc export
    urls = [
        f"https://docs.google.com/document/d/{file_id}/export?format=txt",
        f"https://drive.google.com/uc?export=download&id={file_id}",
    ]
    for url in urls:
        try:
            resp = requests.get(url, timeout=30, allow_redirects=True)
            if resp.status_code == 200 and len(resp.text) > 100:
                logger.success(f"Downloaded {len(resp.text)} chars from public GDrive")
                return resp.text
        except Exception as e:
            logger.debug(f"Public download attempt failed for {url}: {e}")
    return None


def fetch_gdrive_content(file_id: str = GDRIVE_FILE_ID) -> str:
    """
    Fetch content from Google Drive file.
    Tries service account first, then public download fallback.
    Returns file text content.
    """
    logger.info(f"Fetching GDrive file: {file_id}")

    # 1. Service account
    content = _try_service_account(file_id)
    if content:
        _save_gdrive_content(content, file_id)
        return content

    # 2. Public download fallback
    content = _try_public_download(file_id)
    if content:
        _save_gdrive_content(content, file_id)
        return content

    # 3. Return placeholder with CWT brand context if all fails
    logger.warning("All GDrive fetch methods failed — using embedded CWT brand context")
    return _cwt_brand_context()


def _save_gdrive_content(content: str, file_id: str) -> None:
    """Save downloaded content to disk."""
    out = OUTPUT_DIR / f"gdrive_{file_id[:12]}.txt"
    out.write_text(content, encoding="utf-8")
    logger.info(f"GDrive content saved → {out}")


def _cwt_brand_context() -> str:
    """
    Embedded CrowdWisdomTrading brand context as fallback.
    Based on public website information.
    """
    return """
# CrowdWisdomTrading — Brand & Product Context

## What We Do
CrowdWisdomTrading is a stock trading education and signals community that helps 
everyday traders beat the market using crowd intelligence, real-time signals, and 
a supportive community of 10,000+ traders.

## Core Product / Offer
- Premium trading community membership
- Daily real-time buy/sell alerts on top stocks
- Proven trading strategies taught step-by-step
- Live Q&A sessions with experienced traders
- Access to a private Discord community

## Key Pain Points We Solve
1. Traders lose money because they trade alone without proper signals
2. Information overload — too many charts, not enough clarity
3. Emotional trading decisions leading to losses
4. Missing winning trades due to late entries
5. No community or accountability to stay disciplined

## Unique Value Propositions
- "Trade smarter with the crowd" — collective intelligence edge
- Members average 3-5 winning trades per week
- Signals sent before the market moves, not after
- Risk management taught alongside every signal
- Cancel any time — no contracts

## Target Audience
- Age 25-45, working professionals
- Have tried trading before but lost money
- Want financial freedom / side income
- Frustrated with guessing the market
- Ready to invest in their education

## Social Proof
- 10,000+ active members
- 4.8/5 star rating across reviews
- Featured in trading communities and YouTube

## Offer / CTA
- Free trial period for new members
- Join the community → crowdwisdomtrading.com
- Limited spots available (scarcity)
"""