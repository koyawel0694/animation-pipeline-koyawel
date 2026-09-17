#!/usr/bin/env python3
"""
analyze_chapter.py — Read manga pages via vision AI and extract story content.

Sends page images in batches to the local agy vision proxy, extracts dialogue,
scene descriptions, and plot progression. Produces chapter_summary.json that
narrate.py uses to write an informed review.

Usage:
    python3 analyze_chapter.py [--images-dir ./output/images] [--output chapter_summary.json]
                               [--batch-size 5] [--metadata ./output/metadata.json]
"""

import os
import sys
import json
import base64
import argparse
import time
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Vision proxy config
VISION_PROXY = os.environ.get("VISION_PROXY_URL", "http://localhost:8765/v1")
VISION_MODEL = os.environ.get("VISION_MODEL", "antigravity")
VISION_TIMEOUT = int(os.environ.get("VISION_TIMEOUT", "60"))


def load_image_b64(path: str) -> str:
    """Read an image file and return base64-encoded string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def call_vision_proxy(images_b64: list[str], prompt: str, max_tokens: int = 1500) -> str:
    """Send images to the vision proxy and return the text response."""
    content = [{"type": "text", "text": prompt}]
    for i, img_b64 in enumerate(images_b64):
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
        })

    payload = json.dumps({
        "model": VISION_MODEL,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }).encode()

    req = urllib.request.Request(
        f"{VISION_PROXY}/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req, timeout=VISION_TIMEOUT)
    data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


BATCH_PROMPT = """You are reading a manga/manhua/manhwa chapter page by page.
These are pages {start}-{end} of the chapter.

Extract and return ALL of the following in a structured format:

1. DIALOGUE — Every speech bubble, narration box, and thought bubble. Quote the exact text.
2. SCENE DESCRIPTION — What is visually happening in each major panel. Who appears, what they do, the setting.
3. PLOT PROGRESSION — How does this batch of pages advance the story? What events occur, what conflicts develop, what is revealed?

Be thorough and specific. Include ALL dialogue you can read, even sound effects (SFX).
Do NOT summarize vaguely — I need the actual words characters say and specific actions."""


COMPILE_PROMPT = """You have read a full manga/manhua chapter page by page.
Below is the batch-by-batch analysis extracted from the vision AI.

COMPILE a single cohesive chapter summary that captures:

1. STORY SYNOPSIS — A detailed summary of what happens in this chapter (NOT the series synopsis).
   Include specific events, character actions, dialogue quotes, and plot twists.
2. KEY SCENES — The 3-5 most important/memorable moments, with page references.
3. CHARACTER DEVELOPMENT — Who appears, how they change, key decisions they make.
4. THEMES — What the chapter explores (survival, betrayal, growth, etc.)
5. DIALOGUE HIGHLIGHTS — The best/most impactful lines of dialogue.

Do NOT just repeat the batch analyses. Synthesize them into a unified narrative understanding.
Be specific — quote dialogue, reference page numbers, name characters.
Write for a content creator who needs to make an informed video review."""


def analyze_batch(image_paths: list[str], batch_num: int, total_batches: int, start_page: int, max_retries: int = 2) -> dict:
    """Analyze a batch of images and return structured result. Retries on failure."""
    print(f"  [BATCH {batch_num}/{total_batches}] Pages {start_page}-{start_page + len(image_paths) - 1} ({len(image_paths)} pages)...")

    images_b64 = [load_image_b64(p) for p in image_paths]
    prompt = BATCH_PROMPT.format(
        start=start_page,
        end=start_page + len(image_paths) - 1
    )

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            result = call_vision_proxy(images_b64, prompt, max_tokens=1500)
            # Sanity check: reject very short responses (likely error messages)
            if len(result) < 100 and "FAILED" not in result:
                raise ValueError(f"Response too short ({len(result)} chars) — likely a proxy error")
            print(f"  [BATCH {batch_num}] OK — {len(result)} chars extracted")
            return {
                "batch": batch_num,
                "pages": f"{start_page}-{start_page + len(image_paths) - 1}",
                "analysis": result,
            }
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries:
                print(f"  [BATCH {batch_num}] Attempt {attempt} failed: {e} — retrying...")
                time.sleep(2)
            else:
                print(f"  [BATCH {batch_num}] FAILED after {max_retries} attempts: {e}")

    return {
        "batch": batch_num,
        "pages": f"{start_page}-{start_page + len(image_paths) - 1}",
        "analysis": f"[FAILED after {max_retries} attempts: {last_error}]",
        "error": last_error,
    }


def compile_analysis(batch_results: list[dict], metadata: dict) -> str:
    """Send all batch analyses to the vision model for synthesis."""
    print("\n[COMPILE] Synthesizing full chapter analysis...")

    # Build the combined input
    batch_text = ""
    for br in batch_results:
        batch_text += f"\n--- BATCH: Pages {br['pages']} ---\n{br['analysis']}\n"

    title = metadata.get("title", "Unknown")
    synopsis = metadata.get("synopsis", "No synopsis.")

    full_prompt = f"""MANGA: {title}
SERIES SYNOPSIS: {synopsis}

BATCH-BY-BATCH VISION ANALYSIS:
{batch_text}

{COMPILE_PROMPT}"""

    try:
        # Use a text-only call (no images needed for compilation)
        payload = json.dumps({
            "model": VISION_MODEL,
            "messages": [{"role": "user", "content": full_prompt}],
            "max_tokens": 2000,
            "temperature": 0.3,
        }).encode()

        req = urllib.request.Request(
            f"{VISION_PROXY}/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        resp = urllib.request.urlopen(req, timeout=90)
        data = json.loads(resp.read())
        result = data["choices"][0]["message"]["content"]
        print(f"[COMPILE] Done — {len(result)} chars")
        return result
    except Exception as e:
        print(f"[COMPILE] FAILED: {e}")
        # Fallback: just concatenate raw batch results
        return batch_text


def main():
    parser = argparse.ArgumentParser(description="Analyze manga chapter pages via vision AI")
    parser.add_argument("--images-dir", "-i", default="./output/images", help="Directory with page images")
    parser.add_argument("--metadata", "-m", default="./output/metadata.json", help="Path to metadata.json")
    parser.add_argument("--output", "-o", default=None, help="Output path (default: <images-dir>/../chapter_summary.json)")
    parser.add_argument("--batch-size", "-b", type=int, default=5, help="Pages per vision batch")
    parser.add_argument("--parallel", "-p", type=int, default=1, help="Parallel batch requests (default: 1)")
    args = parser.parse_args()

    images_dir = Path(args.images_dir)
    if not images_dir.exists():
        print(f"[ERROR] Images directory not found: {images_dir}")
        sys.exit(1)

    # Collect and sort images
    image_paths = sorted([
        p for p in images_dir.iterdir()
        if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")
    ])
    if not image_paths:
        print(f"[ERROR] No images found in {images_dir}")
        sys.exit(1)

    print(f"[INPUT] {len(image_paths)} pages from {images_dir}")

    # Load metadata
    metadata_path = Path(args.metadata)
    if metadata_path.exists():
        with open(metadata_path) as f:
            metadata = json.load(f)
        print(f"[INPUT] Manga: {metadata.get('title', 'Unknown')}")
    else:
        print(f"[WARN] No metadata found at {metadata_path}, using defaults")
        metadata = {"title": "Unknown", "synopsis": "No synopsis available."}

    # Batch images
    batches = []
    for i in range(0, len(image_paths), args.batch_size):
        batch = image_paths[i:i + args.batch_size]
        batches.append((batch, i + 1))  # (paths, start_page_1indexed)

    total_batches = len(batches)
    print(f"[PLAN] {len(image_paths)} pages → {total_batches} batches of {args.batch_size}")

    # Analyze batches
    print(f"\n[ANALYZE] Reading pages via {VISION_MODEL}...")
    t0 = time.time()

    if args.parallel > 1 and total_batches > 1:
        # Parallel analysis
        print(f"  (parallel: {args.parallel} concurrent requests)")
        batch_results = [None] * total_batches
        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            futures = {}
            for idx, (batch_paths, start_page) in enumerate(batches):
                future = executor.submit(analyze_batch, batch_paths, idx + 1, total_batches, start_page)
                futures[future] = idx
            for future in as_completed(futures):
                idx = futures[future]
                batch_results[idx] = future.result()
    else:
        # Sequential analysis
        batch_results = []
        for idx, (batch_paths, start_page) in enumerate(batches):
            result = analyze_batch(batch_paths, idx + 1, total_batches, start_page)
            batch_results.append(result)
            # Small delay between batches to be nice to the proxy
            if idx < total_batches - 1:
                time.sleep(0.5)

    t_analyze = time.time() - t0
    print(f"\n[ANALYZE] All batches done in {t_analyze:.1f}s")

    # Compile into unified summary
    chapter_analysis = compile_analysis(batch_results, metadata)

    # Build output
    output = {
        "title": metadata.get("title", "Unknown"),
        "author": metadata.get("author", "Unknown"),
        "synopsis": metadata.get("synopsis", ""),
        "chapter": metadata.get("active_chapter", {}),
        "pages_analyzed": len(image_paths),
        "batches": total_batches,
        "analysis_time_seconds": round(t_analyze, 1),
        "chapter_analysis": chapter_analysis,
        "raw_batches": batch_results,
    }

    # Determine output path
    if args.output:
        out_path = Path(args.output)
    else:
        out_path = Path(args.images_dir).parent / "chapter_summary.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n[SAVED] Chapter summary: {out_path}")
    print(f"  Pages analyzed: {len(image_paths)}")
    print(f"  Analysis length: {len(chapter_analysis)} chars")
    print(f"  Time: {t_analyze:.1f}s")


if __name__ == "__main__":
    main()
