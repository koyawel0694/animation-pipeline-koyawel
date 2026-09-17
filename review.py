#!/usr/bin/env python3
"""
review.py — One-command manga review pipeline.

Usage:
    python3 review.py <url> [--length 60] [--voice en-US-GuyNeural] [--output review.mp4]

Example:
    python3 review.py "https://mangadex.org/title/abc123" --length 120

Pipeline:
    1. Scrape manga pages + metadata
    2. Analyze pages via vision AI (reads dialogue, scenes, plot)
    3. Generate informed narration script
    4. Build review video (TTS + Ken Burns + captions)
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

# Ensure we're in the right dir
SCRIPT_DIR = Path(__file__).parent.resolve()
os.chdir(SCRIPT_DIR)

# Load env
env_path = SCRIPT_DIR / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

# Add venv to path
venv = Path.home() / ".venv_manga" / "bin"
if venv.exists():
    os.environ["PATH"] = str(venv) + ":" + os.environ["PATH"]


def run_step(label, cmd, cwd=None):
    """Run a pipeline step and report success/failure."""
    print(f"\n{'='*60}")
    print(f"  STEP: {label}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, cwd=cwd or SCRIPT_DIR, capture_output=False)
    if result.returncode != 0:
        print(f"\n[FAILED] {label} (exit code {result.returncode})")
        sys.exit(result.returncode)
    print(f"[OK] {label}")


def main():
    parser = argparse.ArgumentParser(description="Manga Review Pipeline — one command")
    parser.add_argument("url", nargs="?", default=None, help="Manga page URL (omit to reuse existing scrape)")
    parser.add_argument("--length", "-l", type=int, default=60, help="Target video length (seconds)")
    parser.add_argument("--voice", "-v", default="en-US-GuyNeural", help="TTS voice")
    parser.add_argument("--output", "-o", default=None, help="Output file (default: review_<title>.mp4)")
    parser.add_argument("--chapter", "-c", type=int, default=0, help="Chapter index to use")
    parser.add_argument("--resolution", "-r", default="1080x1920", help="Video resolution (default: TikTok 9:16)")
    parser.add_argument("--vibe", default="analytical", help="Narration vibe: analytical, hype, chill")
    parser.add_argument("--skip-scrape", action="store_true", help="Skip scraping, reuse existing output/")
    parser.add_argument("--skip-analyze", action="store_true", help="Skip vision analysis, reuse existing chapter_summary.json")
    parser.add_argument("--skip-narrate", action="store_true", help="Skip narration, reuse existing narration.txt")
    parser.add_argument("--batch-size", type=int, default=5, help="Pages per vision batch (analyze step)")
    parser.add_argument("--parallel", type=int, default=1, help="Parallel vision requests (analyze step)")
    args = parser.parse_args()

    work_dir = SCRIPT_DIR / "output"
    work_dir.mkdir(exist_ok=True)

    # Step 1: Scrape
    if not args.skip_scrape:
        if not args.url:
            # Check if we have existing scraped data
            if (work_dir / "metadata.json").exists():
                print("[SKIP] No URL provided, using existing scraped data in output/")
            else:
                print("[ERROR] No URL provided and no existing scrape in output/. Provide a manga URL.")
                sys.exit(1)
        else:
            run_step("Scrape manga", [
                sys.executable, "scrape_manga.py", args.url,
                "--output-dir", str(work_dir),
                "--chapter", str(args.chapter),
            ])
    else:
        print("[SKIP] Using existing scraped data in output/")

    # Step 2: Analyze (vision reading)
    metadata_path = work_dir / "metadata.json"
    summary_path = work_dir / "chapter_summary.json"

    if not args.skip_analyze:
        if not metadata_path.exists():
            print("[ERROR] No metadata.json found. Run scrape first.")
            sys.exit(1)

        run_step("Analyze chapter via vision", [
            sys.executable, "analyze_chapter.py",
            "--images-dir", str(work_dir / "images"),
            "--metadata", str(metadata_path),
            "--output", str(summary_path),
            "--batch-size", str(args.batch_size),
            "--parallel", str(args.parallel),
        ])
    else:
        if summary_path.exists():
            print(f"[SKIP] Using existing chapter summary: {summary_path}")
        else:
            print("[WARN] No chapter_summary.json found — narrate will fall back to synopsis-only mode")

    # Step 3: Narrate
    narration_path = work_dir / "narration.txt"

    if not args.skip_narrate:
        if not metadata_path.exists():
            print("[ERROR] No metadata.json found. Run scrape first.")
            sys.exit(1)

        # narrate.py auto-detects chapter_summary.json next to metadata
        run_step("Generate narration", [
            sys.executable, "narrate.py",
            str(metadata_path),
            "--output", str(narration_path),
            "--length", str(args.length),
            "--vibe", args.vibe,
        ])
    else:
        print(f"[SKIP] Using existing narration: {narration_path}")

    # Determine output filename
    if not args.output:
        with open(metadata_path) as f:
            meta = json.load(f)
        title_safe = meta.get("title", "review")[:40]
        title_safe = "".join(c if c.isalnum() or c in " -_" else "" for c in title_safe)
        title_safe = title_safe.strip().replace(" ", "_")
        output_file = str(SCRIPT_DIR / f"review_{title_safe}.mp4")
    else:
        output_file = args.output

    # Step 4: Build video
    run_step("Build review video", [
        sys.executable, "build_review.py",
        str(work_dir / "images"),
        str(narration_path),
        "--output", output_file,
        "--voice", args.voice,
        "--resolution", args.resolution,
    ])

    print(f"\n{'='*60}")
    print(f"  DONE! Review video ready:")
    print(f"  {output_file}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
