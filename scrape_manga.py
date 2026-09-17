#!/usr/bin/env python3
"""
scrape_manga.py — Download manga page images + extract metadata from a URL.
Uses requests + BeautifulSoup for static sites, or falls back to manual input.

Usage:
    python3 scrape_manga.py <url> [--output-dir ./output]

Output:
    <output-dir>/metadata.json  — title, author, synopsis, chapter info
    <output-dir>/images/        — downloaded page images (page_001.jpg etc.)
"""

import os
import sys
import json
import time
import re
import argparse
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse

# Try BeautifulSoup, fall back gracefully
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# MangaDex API base
MANGADEX_API = "https://api.mangadex.org"


def fetch_mangadex_id(url: str) -> str:
    """Extract manga ID from MangaDex URL."""
    # Patterns: /title/xxx-uuid, /manga/xxx-uuid
    m = re.search(r'/(?:title|manga)/([0-9a-f-]{36})', url)
    if m:
        return m.group(1)
    return None


def mangadex_fetch_info(manga_id: str) -> dict:
    """Fetch manga info from MangaDex API."""
    r = requests.get(f"{MANGADEX_API}/manga/{manga_id}", headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()["data"]
    attrs = data["attributes"]

    title = attrs.get("title", {})
    title_en = title.get("en") or title.get("ja-ro") or title.get("ja") or list(title.values())[0] if title else "Unknown"

    # Synopsis
    desc = attrs.get("description", {})
    synopsis = desc.get("en") or list(desc.values())[0] if desc else "No synopsis available."

    # Tags
    tags = [t["attributes"]["name"].get("en", t["attributes"]["name"].get("ja", "")) for t in attrs.get("tags", [])]

    # Author
    author = "Unknown"
    relationships = data.get("relationships", [])
    for rel in relationships:
        if rel.get("type") == "author":
            # Need separate call for author name
            pass

    # Try to get author from relationships
    author_id = None
    for rel in relationships:
        if rel["type"] == "author":
            author_id = rel["id"]
            break
    if author_id:
        try:
            ar = requests.get(f"{MANGADEX_API}/author/{author_id}", headers=HEADERS, timeout=10)
            if ar.status_code == 200:
                author = ar.json()["data"]["attributes"].get("name", "Unknown")
        except Exception:
            pass

    # Status
    status = attrs.get("status", "unknown")

    # Get first chapter ID for preview
    ch_r = requests.get(
        f"{MANGADEX_API}/manga/{manga_id}/feed",
        headers=HEADERS,
        params={"limit": 10, "translatedLanguage[]": "en", "order[chapter]": "asc"},
        timeout=30,
    )
    chapters = []
    if ch_r.status_code == 200:
        for ch in ch_r.json().get("data", []):
            ch_attrs = ch["attributes"]
            chapters.append({
                "id": ch["id"],
                "chapter": ch_attrs.get("chapter", "?"),
                "title": ch_attrs.get("title", ""),
            })

    return {
        "source": "mangadex",
        "url": f"https://mangadex.org/title/{manga_id}",
        "title": title_en,
        "author": author,
        "synopsis": synopsis,
        "tags": tags,
        "status": status,
        "chapters": chapters[:10],
    }


def mangadex_download_chapter_images(chapter_id: str, output_dir: Path, limit: int = 30) -> list[str]:
    """Download page images for a chapter from MangaDex."""
    # Get chapter server + page data
    r = requests.get(f"{MANGADEX_API}/at-home/server/{chapter_id}", headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    base_url = data["baseUrl"]
    chapter_hash = data["chapter"]["hash"]
    pages = data["chapter"]["data"]

    images = []
    for i, page in enumerate(pages[:limit]):
        img_url = f"{base_url}/data/{chapter_hash}/{page}"
        ext = Path(page).suffix or ".jpg"
        out_path = output_dir / f"page_{i+1:03d}{ext}"
        try:
            img_r = requests.get(img_url, headers=HEADERS, timeout=60)
            img_r.raise_for_status()
            out_path.write_bytes(img_r.content)
            images.append(str(out_path))
            print(f"  [OK] page {i+1}/{min(len(pages), limit)}: {out_path.name}")
        except Exception as e:
            print(f"  [FAIL] page {i+1}: {e}")
        time.sleep(0.3)  # rate limit courtesy

    return images


def scrape_generic_url(url: str, output_dir: Path) -> dict:
    """Generic scraper — downloads all images from a page. Fallback for non-MangaDex sites."""
    if not HAS_BS4:
        print("[WARN] BeautifulSoup not installed. Install with: pip install beautifulsoup4")
        print("[INFO] Falling back to manual image list mode.")
        return {"source": "generic", "url": url, "title": "Unknown", "images": []}

    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.title.string.strip() if soup.title else "Unknown"

    # Find all images
    images = []
    img_dir = output_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    for i, img in enumerate(soup.find_all("img")):
        src = img.get("src") or img.get("data-src")
        if not src:
            continue
        full_url = urljoin(url, src)
        ext = Path(urlparse(full_url).path).suffix or ".jpg"
        out_path = img_dir / f"page_{i+1:03d}{ext}"
        try:
            img_r = requests.get(full_url, headers=HEADERS, timeout=30)
            if img_r.status_code == 200 and len(img_r.content) > 1000:  # skip tiny icons
                out_path.write_bytes(img_r.content)
                images.append(str(out_path))
                print(f"  [OK] {out_path.name}")
        except Exception:
            pass
        time.sleep(0.2)

    return {
        "source": "generic",
        "url": url,
        "title": title,
        "images": images,
    }


def main():
    parser = argparse.ArgumentParser(description="Scrape manga page images + metadata")
    parser.add_argument("url", help="Manga page URL (MangaDex or generic)")
    parser.add_argument("--output-dir", "-o", default="./manga_output", help="Output directory")
    parser.add_argument("--chapter", "-c", type=int, default=0, help="Chapter index to download (0 = first)")
    parser.add_argument("--max-pages", "-m", type=int, default=30, help="Max pages to download")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    img_dir = output_dir / "images"
    img_dir.mkdir(exist_ok=True)

    # Detect MangaDex
    manga_id = fetch_mangadex_id(args.url)

    if manga_id:
        print(f"[MangaDex] Fetching info for {manga_id}...")
        info = mangadex_fetch_info(manga_id)
        print(f"  Title: {info['title']}")
        print(f"  Author: {info['author']}")
        print(f"  Chapters found: {len(info['chapters'])}")

        if info["chapters"]:
            ch = info["chapters"][min(args.chapter, len(info["chapters"])-1)]
            print(f"\n[DOWNLOAD] Chapter {ch['chapter']}: {ch['id']}")
            images = mangadex_download_chapter_images(ch["id"], img_dir, limit=args.max_pages)
            info["downloaded_images"] = images
            info["active_chapter"] = ch
        else:
            print("[WARN] No English chapters found.")
            info["downloaded_images"] = []
    else:
        print(f"[GENERIC] Scraping {args.url}...")
        info = scrape_generic_url(args.url, img_dir)

    # Save metadata
    meta_path = output_dir / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    print(f"\n[SAVED] Metadata: {meta_path}")
    print(f"[SAVED] Images: {len(info.get('downloaded_images', info.get('images', [])))} files in {img_dir}")

    return info


if __name__ == "__main__":
    main()
