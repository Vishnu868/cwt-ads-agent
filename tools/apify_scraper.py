"""
tools/apify_scraper.py
Scrapes Meta Ads Library for CrowdWisdomTrading niche ads using Apify.
Returns structured ad data for the last N days.
"""
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from apify_client import ApifyClient
from loguru import logger

from config.settings import (
    APIFY_API_TOKEN,
    NICHE_KEYWORDS,
    ADS_LOOKBACK_DAYS,
    MAX_ADS_TO_ANALYSE,
    OUTPUT_DIR,
    TARGET_WEBSITE,
)


# ─── Apify Actor IDs ─────────────────────────────────────────────────────────
META_ADS_ACTOR = "curious_coder/facebook-ads-library-scraper"
FALLBACK_ACTOR = "apify/facebook-ads-scraper"


def _build_search_terms() -> list[str]:
    """Build search queries combining brand + niche keywords."""
    terms = [TARGET_WEBSITE.replace(".com", "")]
    terms += NICHE_KEYWORDS[:5]   # top 5 niche keywords
    return terms


def _is_recent(date_str: str, days: int = ADS_LOOKBACK_DAYS) -> bool:
    """Check if an ad was active in the last N days."""
    if not date_str:
        return True  # include if date unknown
    try:
        cutoff = datetime.now() - timedelta(days=days)
        ad_date = datetime.fromisoformat(date_str.replace("Z", "+00:00").replace("+00:00", ""))
        return ad_date >= cutoff
    except Exception:
        return True


def _normalise_ad(raw: dict) -> dict:
    """Normalise raw Apify ad record into a consistent schema."""
    return {
        "id": raw.get("id") or raw.get("adArchiveID") or raw.get("ad_archive_id", ""),
        "page_name": raw.get("pageName") or raw.get("page_name", ""),
        "ad_text": (
            raw.get("adCard", {}).get("body", "")
            or raw.get("snapshot", {}).get("body", {}).get("message", "")
            or raw.get("ad_creative_bodies", [""])[0]
            or raw.get("body", "")
        ),
        "headline": (
            raw.get("adCard", {}).get("title", "")
            or raw.get("snapshot", {}).get("title", "")
            or raw.get("ad_creative_link_titles", [""])[0]
            or ""
        ),
        "cta": (
            raw.get("adCard", {}).get("callToAction", "")
            or raw.get("snapshot", {}).get("cta_type", "")
            or ""
        ),
        "start_date": raw.get("startDate") or raw.get("start_date", ""),
        "end_date": raw.get("endDate") or raw.get("end_date", ""),
        "platforms": raw.get("publisherPlatforms") or raw.get("publisher_platforms", []),
        "impressions": raw.get("impressionsWithIndex", {}) or {},
        "media_type": raw.get("adCard", {}).get("type", "") or raw.get("ad_creative_link_captions", [""])[0] or "",
        "url": (
            raw.get("adCard", {}).get("linkUrl", "")
            or raw.get("snapshot", {}).get("link_url", "")
            or ""
        ),
        "raw": raw,
    }


def scrape_meta_ads() -> list[dict]:
    """
    Run Apify Meta Ads Library scraper for the CWT niche.
    Returns normalised list of ad dicts.
    """
    client = ApifyClient(APIFY_API_TOKEN)
    search_terms = _build_search_terms()
    all_ads: list[dict] = []

    logger.info(f"Starting Meta Ads scrape | terms={search_terms} | lookback={ADS_LOOKBACK_DAYS}d")

    for term in search_terms:
        logger.debug(f"Scraping term: '{term}'")
        try:
            run_input = {
                "searchTerms": [term],
                "country": "US",
                "maxResults": MAX_ADS_TO_ANALYSE,
                "activeStatus": "active",
                "adType": "all",
            }

            run = client.actor(META_ADS_ACTOR).call(run_input=run_input, timeout_secs=120)
            dataset_id = run.get("defaultDatasetId")

            if not dataset_id:
                logger.warning(f"No dataset returned for term '{term}'")
                continue

            items = list(client.dataset(dataset_id).iterate_items())
            logger.info(f"  → Got {len(items)} raw ads for '{term}'")

            for item in items:
                normalised = _normalise_ad(item)
                if _is_recent(normalised["start_date"]):
                    all_ads.append(normalised)

            time.sleep(2)  # polite delay between runs

        except Exception as exc:
            logger.error(f"Apify run failed for '{term}': {exc}")
            # Try fallback approach - direct Meta Ads Library URL scraping
            try:
                fallback_ads = _fallback_scrape(client, term)
                all_ads.extend(fallback_ads)
            except Exception as fb_exc:
                logger.error(f"Fallback also failed: {fb_exc}")

    # Deduplicate by ad ID
    seen: set[str] = set()
    unique_ads: list[dict] = []
    for ad in all_ads:
        key = ad["id"] or ad["ad_text"][:50]
        if key and key not in seen:
            seen.add(key)
            unique_ads.append(ad)

    # Filter out ads with no text
    unique_ads = [a for a in unique_ads if a["ad_text"] or a["headline"]]
    unique_ads = unique_ads[:MAX_ADS_TO_ANALYSE]

    logger.success(f"Scraped {len(unique_ads)} unique ads after dedup/filter")
    return unique_ads


def _fallback_scrape(client, term):
    url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q={term}&search_type=keyword_unordered"
    run_input = {
        "startUrls": [{"url": url}],
        "maxResults": 10,
    }
    run = client.actor("apify/facebook-ads-scraper").call(run_input=run_input, timeout_secs=90)
    dataset_id = run.get("defaultDatasetId", "")
    if not dataset_id:
        return []
    items = list(client.dataset(dataset_id).iterate_items())
    return [_normalise_ad(i) for i in items]


def save_ads_to_json(ads: list[dict], filename: str = "scraped_ads.json") -> Path:
    """Save ads list to OUTPUT_DIR/filename and return path."""
    output_path = OUTPUT_DIR / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "scraped_at": datetime.now().isoformat(),
                "total_ads": len(ads),
                "lookback_days": ADS_LOOKBACK_DAYS,
                "ads": ads,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    logger.success(f"Saved {len(ads)} ads → {output_path}")
    return output_path