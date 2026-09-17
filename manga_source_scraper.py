#!/usr/bin/env python3
"""
manga_source_scraper.py — Discover and scrape manga/manhua/manhwa chapters.

Workflow (Nodes 1 to 4):
  1. User enters link or title.
  2. Finder discovers source materials via MangaDex API / web sources.
  3. Interactive or CLI selection: asks user how many chapters to scrape.
  4. Scrapes requested chapters into structured directories ready for processing.

Usage:
  Interactive:
    python3 manga_source_scraper.py
  Non-interactive:
    python3 manga_source_scraper.py --query "From Goblin to Goblin God" --chapters 1 --max-pages 15
    python3 manga_source_scraper.py --url "https://mangadex.org/title/a958abd8-745d-4f47-9c4d-89abae30f5df" --chapters 2
"""

import os
import sys
import json
import time
import re
import argparse
from pathlib import Path
from urllib.parse import urlparse, urljoin
import requests

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

MANGADEX_API = "https://api.mangadex.org"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


def sanitize_filename(name: str) -> str:
    """Convert title string into safe directory name."""
    clean = re.sub(r"[^\w\s-]", "", name).strip().lower()
    return re.sub(r"[-\s]+", "-", clean)[:60] or "manga"


def extract_mangadex_id(url_or_id: str) -> tuple[str, str]:
    """
    Extract (entity_type, entity_id) from MangaDex URL or ID string.
    Returns ('manga', uuid), ('chapter', uuid), or ('query', input_str).
    """
    url_or_id = url_or_id.strip()
    uuid_pattern = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"

    # Manga URL pattern
    m_title = re.search(rf"/(?:title|manga)/({uuid_pattern})", url_or_id)
    if m_title:
        return ("manga", m_title.group(1))

    # Chapter URL pattern
    m_ch = re.search(rf"/chapter/({uuid_pattern})", url_or_id)
    if m_ch:
        return ("chapter", m_ch.group(1))

    # Raw UUID
    if re.fullmatch(uuid_pattern, url_or_id):
        return ("manga", url_or_id)

    return ("query", url_or_id)


def search_manga(query: str, limit: int = 5) -> list[dict]:
    """Search MangaDex for titles matching query."""
    params = {
        "title": query,
        "limit": limit,
        "includes[]": ["cover_art", "author", "artist"],
        "order[relevance]": "desc",
    }
    resp = requests.get(f"{MANGADEX_API}/manga", params=params, headers=HEADERS, timeout=25)
    resp.raise_for_status()
    items = resp.json().get("data", [])

    results = []
    for item in items:
        m_id = item["id"]
        attrs = item.get("attributes", {})
        title_dict = attrs.get("title", {})
        # Prefer English, then transliterated, then whatever title exists
        title = (
            title_dict.get("en")
            or title_dict.get("ja-ro")
            or title_dict.get("ko-ro")
            or title_dict.get("zh-ro")
            or (list(title_dict.values())[0] if title_dict else "Unknown Title")
        )

        alt_titles = []
        for alt in attrs.get("altTitles", []):
            alt_titles.extend(alt.values())

        desc_dict = attrs.get("description", {})
        synopsis = desc_dict.get("en") or (list(desc_dict.values())[0] if desc_dict else "")

        # Extract authors
        authors = []
        for rel in item.get("relationships", []):
            if rel.get("type") in ("author", "artist"):
                rel_attrs = rel.get("attributes", {})
                if rel_attrs and "name" in rel_attrs:
                    authors.append(rel_attrs["name"])

        results.append({
            "id": m_id,
            "title": title,
            "alt_titles": alt_titles[:4],
            "synopsis": synopsis,
            "author": ", ".join(dict.fromkeys(authors)) if authors else "Unknown",
            "status": attrs.get("status", "unknown"),
            "url": f"https://mangadex.org/title/{m_id}",
        })

    return results


def get_manga_by_id(manga_id: str) -> dict:
    """Fetch manga info directly by manga ID."""
    params = {"includes[]": ["author", "artist"]}
    resp = requests.get(f"{MANGADEX_API}/manga/{manga_id}", params=params, headers=HEADERS, timeout=25)
    resp.raise_for_status()
    data = resp.json()["data"]
    attrs = data.get("attributes", {})
    title_dict = attrs.get("title", {})
    title = (
        title_dict.get("en")
        or title_dict.get("ja-ro")
        or title_dict.get("ko-ro")
        or title_dict.get("zh-ro")
        or (list(title_dict.values())[0] if title_dict else "Unknown Title")
    )
    desc_dict = attrs.get("description", {})
    synopsis = desc_dict.get("en") or (list(desc_dict.values())[0] if desc_dict else "")

    authors = []
    for rel in data.get("relationships", []):
        if rel.get("type") in ("author", "artist"):
            rel_attrs = rel.get("attributes", {})
            if rel_attrs and "name" in rel_attrs:
                authors.append(rel_attrs["name"])

    return {
        "id": manga_id,
        "title": title,
        "synopsis": synopsis,
        "author": ", ".join(dict.fromkeys(authors)) if authors else "Unknown",
        "status": attrs.get("status", "unknown"),
        "url": f"https://mangadex.org/title/{manga_id}",
    }


def list_chapters(manga_id: str, language: str = "en") -> list[dict]:
    """Fetch and sort available chapters for a manga in requested language."""
    params = {
        "translatedLanguage[]": language,
        "order[chapter]": "asc",
        "limit": 100,
        "includes[]": ["scanlation_group"],
    }
    resp = requests.get(f"{MANGADEX_API}/manga/{manga_id}/feed", params=params, headers=HEADERS, timeout=25)
    if resp.status_code == 400:
        return []
    resp.raise_for_status()
    raw_chapters = resp.json().get("data", [])

    # Filter out external links (which have 0 pages on MangaDex) and deduplicate by chapter number
    chapters_by_num = {}
    for ch in raw_chapters:
        attrs = ch.get("attributes", {})
        pages = attrs.get("pages", 0)
        ext_url = attrs.get("externalUrl")
        if ext_url and pages == 0:
            continue  # external platform redirect

        ch_num_raw = attrs.get("chapter")
        if not ch_num_raw:
            continue

        try:
            ch_num_float = float(ch_num_raw)
        except ValueError:
            ch_num_float = 9999.0

        if ch_num_raw not in chapters_by_num or pages > chapters_by_num[ch_num_raw]["pages"]:
            group_name = "Unknown"
            for rel in ch.get("relationships", []):
                if rel.get("type") == "scanlation_group" and rel.get("attributes"):
                    group_name = rel["attributes"].get("name", "Unknown")

            chapters_by_num[ch_num_raw] = {
                "id": ch["id"],
                "chapter": ch_num_raw,
                "sort_num": ch_num_float,
                "title": attrs.get("title") or f"Chapter {ch_num_raw}",
                "pages": pages,
                "group": group_name,
            }

    sorted_chapters = sorted(chapters_by_num.values(), key=lambda x: x["sort_num"])
    return sorted_chapters


def download_chapter(chapter_info: dict, manga_meta: dict, output_dir: Path, max_pages: int = None) -> dict:
    """Download pages for a chapter and save metadata."""
    chapter_id = chapter_info["id"]
    ch_num = chapter_info.get("chapter", "1")
    ch_dir = output_dir / f"ch{ch_num}"
    images_dir = ch_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[DOWNLOAD] Chapter {ch_num} (ID: {chapter_id}) -> {ch_dir}")

    # Fetch at-home server info
    at_home_url = f"{MANGADEX_API}/at-home/server/{chapter_id}"
    resp = requests.get(at_home_url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    server_data = resp.json()

    base_url = server_data.get("baseUrl")
    ch_data = server_data.get("chapter", {})
    ch_hash = ch_data.get("hash")
    filenames = ch_data.get("data", [])

    if not filenames:
        filenames = ch_data.get("dataSaver", [])

    if max_pages and max_pages > 0:
        filenames = filenames[:max_pages]

    total_pages = len(filenames)
    print(f"[PAGES] Downloading {total_pages} pages...")

    saved_images = []
    for i, fname in enumerate(filenames, start=1):
        ext = Path(fname).suffix or ".jpg"
        out_file = images_dir / f"page_{i:03d}{ext}"

        if out_file.exists() and out_file.stat().st_size > 1000:
            saved_images.append(str(out_file.resolve()))
            print(f"  [{i}/{total_pages}] Already downloaded: {out_file.name}")
            continue

        page_url = f"{base_url}/data/{ch_hash}/{fname}"
        downloaded = False
        for attempt in range(3):
            try:
                img_resp = requests.get(page_url, headers=HEADERS, timeout=20)
                if img_resp.status_code == 200 and len(img_resp.content) > 1000:
                    out_file.write_bytes(img_resp.content)
                    saved_images.append(str(out_file.resolve()))
                    print(f"  [{i}/{total_pages}] Saved: {out_file.name} ({len(img_resp.content)//1024} KB)")
                    downloaded = True
                    break
            except Exception as e:
                time.sleep(1 + attempt)

        if not downloaded:
            print(f"  [{i}/{total_pages}] Warning: failed to download page {fname}")

        time.sleep(0.15)

    # Save chapter metadata.json
    ch_meta = {
        "title": manga_meta.get("title", "Unknown"),
        "author": manga_meta.get("author", "Unknown"),
        "synopsis": manga_meta.get("synopsis", ""),
        "manga_id": manga_meta.get("id"),
        "manga_url": manga_meta.get("url"),
        "chapter": {
            "id": chapter_id,
            "chapter": ch_num,
            "title": chapter_info.get("title"),
            "group": chapter_info.get("group"),
        },
        "pages_count": len(saved_images),
        "images": saved_images,
        "downloaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    meta_file = ch_dir / "metadata.json"
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(ch_meta, f, indent=2, ensure_ascii=False)

    print(f"[OK] Chapter {ch_num} saved: {len(saved_images)} pages, metadata at {meta_file}")
    return ch_meta



# ---------------------------------------------------------------------------
# FALLBACK: Generic webtoon reader scraping (for titles not on MangaDex)
# ---------------------------------------------------------------------------

FALLBACK_READER_PATTERNS = [
    # Sites following the Madara / ThemeMars WordPress reader layout with
    # predictable URL shapes. {slug} = title slug, {num} = chapter number.
    "https://theinvestorwhoseesthefuture.com/manga/{slug}-chapter-{num}/",
    "https://manhwatop.com/manga/{slug}/chapter-{num}/",
    "https://manhuatop.org/manhua/{slug}-top/chapter-{num}/",
    "https://kingofshojo.com/{slug}-chapter-{num}/",
]


def slugify_for_readers(title: str) -> str:
    """Convert a title into a reader-site slug."""
    clean = re.sub(r"[^\w\s-]", "", title, flags=re.UNICODE).strip().lower()
    return re.sub(r"[\s_]+", "-", clean)


def fetch_reader_chapter_images(chapter_url: str) -> list[str]:
    """Scrape page image URLs from a generic WordPress/Madara manga reader."""
    if not HAS_BS4:
        return []
    r = requests.get(chapter_url, headers={**HEADERS, "Referer": chapter_url}, timeout=30)
    if r.status_code != 200:
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    urls = []
    seen = set()
    for img in soup.select(".reading-content img, .entry-content img, .read-container img, .rdminimal img"):
        src = img.get("src") or img.get("data-src") or ""
        src = urljoin(chapter_url, src.strip())
        if src.startswith("http") and re.search(r"\.(webp|jpg|jpeg|png)(\?|$)", src, re.I) and src not in seen:
            seen.add(src)
            urls.append(src)
    return urls


def download_generic_images(image_urls: list[str], images_dir: Path, referer: str) -> list[str]:
    """Download a list of remote images into images_dir; returns saved paths."""
    images_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for i, img_url in enumerate(image_urls, start=1):
        ext = Path(urlparse(img_url).path).suffix or ".jpg"
        out_file = images_dir / f"page_{i:03d}{ext}"
        if out_file.exists() and out_file.stat().st_size > 1000:
            saved.append(str(out_file.resolve()))
            continue
        ok = False
        for attempt in range(3):
            try:
                r = requests.get(img_url, headers={**HEADERS, "Referer": referer}, timeout=30)
                if r.status_code == 200 and len(r.content) > 1000:
                    out_file.write_bytes(r.content)
                    saved.append(str(out_file.resolve()))
                    ok = True
                    break
            except Exception:
                time.sleep(1 + attempt)
        if not ok:
            print(f"  [FAIL] page {i}: {img_url}")
        time.sleep(0.15)
    return saved


def scrape_fallback_chapters(title: str, num_chapters: int, manga_output_dir: Path, max_pages: int = None, start_chapter: int = 1) -> list[dict]:
    """
    Fallback source when MangaDex has no chapters: probe known webtoon reader
    sites for the title slug and download chapters from start_chapter to (start_chapter + num_chapters - 1).
    """
    slug = slugify_for_readers(title)
    print(f"[FALLBACK] Probing web readers for slug: {slug}")

    working_pattern = None
    for pattern in FALLBACK_READER_PATTERNS:
        probe_url = pattern.format(slug=slug, num=start_chapter)
        try:
            r = requests.get(probe_url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                images = fetch_reader_chapter_images(probe_url)
                if images:
                    working_pattern = pattern
                    print(f"[FALLBACK] Reader works: {probe_url} ({len(images)} pages in ch{start_chapter})")
                    break
        except Exception:
            continue

    if not working_pattern:
        print("[FALLBACK] No known reader site responded for this title.")
        return []

    results = []
    end_chapter = start_chapter + num_chapters
    for ch_num in range(start_chapter, end_chapter):
        chapter_url = working_pattern.format(slug=slug, num=ch_num)
        print(f"\n[DOWNLOAD] Fallback chapter {ch_num}: {chapter_url}")
        images = fetch_reader_chapter_images(chapter_url)
        if not images:
            print(f"  [WARN] No images found for chapter {ch_num} — stopping.")
            break
        if max_pages:
            images = images[:max_pages]

        ch_dir = manga_output_dir / f"ch{ch_num}"
        saved = download_generic_images(images, ch_dir / "images", referer=chapter_url)

        ch_meta = {
            "title": title,
            "author": "Unknown (web reader fallback)",
            "synopsis": "",
            "manga_id": None,
            "manga_url": chapter_url.rsplit("/chapter-", 1)[0] + "/",
            "chapter": {
                "id": f"fallback-ch{ch_num}",
                "chapter": str(ch_num),
                "title": f"Chapter {ch_num}",
                "group": "web-reader",
            },
            "source_url": chapter_url,
            "pages_count": len(saved),
            "images": saved,
            "downloaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        meta_file = ch_dir / "metadata.json"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(ch_meta, f, indent=2, ensure_ascii=False)
        print(f"[OK] Chapter {ch_num} saved: {len(saved)} pages -> {meta_file}")
        results.append(ch_meta)

    return results


def run_pipeline_source_flow(input_target: str = None, num_chapters: int = None, output_base: Path = None, max_pages_per_ch: int = None, start_chapter: int = 1) -> list[dict]:
    """
    Executes Nodes 1 to 4 of the pipeline:
      - Accepts input (link or title)
      - Finds source material
      - Interactively asks or uses chapter count
      - Scrapes the chapters into structured output directories
    """
    if output_base is None:
        output_base = Path("/home/john/manga-reviews/output")

    # Node 1 & 2: User provides title or link -> Hermes finds source
    if not input_target:
        print("\n" + "=" * 60)
        print("  HERMES MANGA SOURCE DISCOVERY")
        print("=" * 60)
        print("Paste a manga/manhua/manhwa link or title:")
        try:
            input_target = input("> ").strip()
        except EOFError:
            print("\n[ERROR] No input provided.")
            return []

    if not input_target:
        print("[ERROR] Empty link/title provided.")
        return []

    # Check if input URL has chapter number
    m_ch_url = re.search(r"chapter-(\d+)", input_target, re.IGNORECASE)
    if m_ch_url and start_chapter == 1:
        start_chapter = int(m_ch_url.group(1))

    print(f"\n[SEARCH] Resolving source materials for: {input_target}")
    kind, val = extract_mangadex_id(input_target)

    manga_info = None
    if kind == "manga":
        manga_info = get_manga_by_id(val)
    elif kind == "chapter":
        # Resolve chapter to manga
        c_resp = requests.get(f"{MANGADEX_API}/chapter/{val}", params={"includes[]": ["manga"]}, headers=HEADERS, timeout=25)
        c_resp.raise_for_status()
        m_rel = next((r for r in c_resp.json()["data"]["relationships"] if r["type"] == "manga"), None)
        if m_rel:
            manga_info = get_manga_by_id(m_rel["id"])
        else:
            raise RuntimeError(f"Could not resolve manga for chapter {val}")
    else:
        results = search_manga(val, limit=5)
        if not results:
            print(f"[ERROR] No results found on MangaDex for '{val}'.")
            return []

        print(f"\nFound {len(results)} matching titles:")
        for idx, res in enumerate(results, start=1):
            print(f"  [{idx}] {res['title']} ({res['status']}) by {res['author']}")
            if res.get("alt_titles"):
                print(f"      Alt: {', '.join(res['alt_titles'][:2])}")

        # If non-interactive or only 1, pick 1
        if len(results) == 1 or not sys.stdin.isatty():
            manga_info = results[0]
            print(f"[AUTO-SELECT] Selected: {manga_info['title']}")
        else:
            print("\nSelect manga number (default 1):")
            sel = input("> ").strip()
            sel_idx = int(sel) - 1 if (sel.isdigit() and 1 <= int(sel) <= len(results)) else 0
            manga_info = results[sel_idx]

    print("\n" + "-" * 60)
    print(f"SELECTED TITLE: {manga_info['title']}")
    print(f"AUTHOR:         {manga_info['author']}")
    print(f"STATUS:         {manga_info['status']}")
    print(f"URL:            {manga_info['url']}")
    if manga_info.get("synopsis"):
        print(f"SYNOPSIS:       {manga_info['synopsis'][:200]}...")
    print("-" * 60)

    # Node 3: List chapters and ask how many chapters to scrape
    print("\n[CHAPTERS] Fetching English chapter list...")
    chapters = list_chapters(manga_info["id"], language="en")
    if not chapters:
        print("[WARN] No English scanlations found on MangaDex.")
        # MangaDex has metadata but no downloadable chapters — try web reader fallback
        print("[FALLBACK] Trying known webtoon reader sites...")
        slug = sanitize_filename(manga_info["title"])
        manga_output_dir = output_base / slug
        fallback_results = scrape_fallback_chapters(
            manga_info["title"], num_chapters or 1, manga_output_dir, max_pages=max_pages_per_ch, start_chapter=start_chapter
        )
        if fallback_results:
            print(f"\n[COMPLETE] Fallback scrape succeeded: {len(fallback_results)} chapter(s) into {manga_output_dir}")
            return fallback_results
        print("[ERROR] No downloadable chapters found for this title on MangaDex or fallback readers.")
        return []

    print(f"[INFO] Found {len(chapters)} available chapters:")
    for ch in chapters[:8]:
        print(f"  - Chapter {ch['chapter']}: {ch['title']} ({ch['pages']} pages, group: {ch['group']})")
    if len(chapters) > 8:
        print(f"  ... and {len(chapters) - 8} more chapters.")

    # Node 3 prompt: "You will ask me if how many chapters i want to scrape"
    if num_chapters is None:
        if sys.stdin.isatty():
            print(f"\nHow many chapters do you want to scrape? (1-{len(chapters)}, default 1):")
            ch_input = input("> ").strip()
            num_chapters = int(ch_input) if ch_input.isdigit() and int(ch_input) > 0 else 1
        else:
            num_chapters = 1

    selected_chapters = chapters[:num_chapters]
    print(f"\n[ORCHESTRATOR] Preparing to scrape {len(selected_chapters)} chapter(s):")
    for sc in selected_chapters:
        print(f"  * Chapter {sc['chapter']} ({sc['pages']} pages)")

    slug = sanitize_filename(manga_info["title"])
    manga_output_dir = output_base / slug

    scraped_chapters = []
    for sc in selected_chapters:
        res = download_chapter(sc, manga_info, manga_output_dir, max_pages=max_pages_per_ch)
        scraped_chapters.append(res)

    print(f"\n[COMPLETE] Successfully scraped {len(scraped_chapters)} chapter(s) into {manga_output_dir}")
    return scraped_chapters


def main():
    parser = argparse.ArgumentParser(description="Manga Source Finder and Scraper")
    parser.add_argument("--query", "-q", help="Manga title query")
    parser.add_argument("--url", "-u", help="MangaDex URL or chapter URL")
    parser.add_argument("--chapters", "-c", type=int, default=None, help="How many chapters to scrape")
    parser.add_argument("--start-chapter", "-s", type=int, default=1, help="Chapter number to start scraping from (default 1)")
    parser.add_argument("--max-pages", "-m", type=int, default=None, help="Max pages per chapter to scrape")
    parser.add_argument("--output-dir", "-o", default="/home/john/manga-reviews/output", help="Base output directory")
    args = parser.parse_args()

    target = args.url or args.query
    out_dir = Path(args.output_dir).resolve()
    run_pipeline_source_flow(
        input_target=target,
        num_chapters=args.chapters,
        output_base=out_dir,
        max_pages_per_ch=args.max_pages,
        start_chapter=args.start_chapter,
    )


if __name__ == "__main__":
    main()
