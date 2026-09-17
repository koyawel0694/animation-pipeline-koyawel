#!/usr/bin/env python3
"""
narrate.py — Generate narration script for a manga review.

Two modes:
  1. WITH chapter_summary.json (vision-analyzed): Rich, story-informed narration
  2. WITHOUT (fallback): Synopsis-only narration (legacy mode)

Usage:
    python3 narrate.py <metadata.json> [--output narration.txt] [--length 60]
    python3 narrate.py --summary <chapter_summary.json> [--output narration.txt] [--length 60]
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path


def load_env():
    """Load env vars from .env file."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()


def generate_narration_from_summary(summary: dict, target_seconds: int = 60, voice_vibe: str = "analytical") -> str:
    """Generate narration using the vision-analyzed chapter summary."""
    api_key = os.environ.get("OPENCODE_GO_API_KEY")
    base_url = os.environ.get("OPENCODE_GO_BASE_URL", "https://opencode.ai/zen/go/v1")
    model = os.environ.get("OPENCODE_GO_MODEL", "hy3")

    if not api_key:
        print("[ERROR] OPENCODE_GO_API_KEY not set. Check .env or environment.")
        sys.exit(1)

    title = summary.get("title", "Unknown")
    author = summary.get("author", "Unknown")
    chapter_analysis = summary.get("chapter_analysis", "No analysis available.")

    word_count = 175  # tight, punchy — every word earns its place

    prompt = f"""You are a manga/manhua/manhwa SHORT-FORM video reviewer writing a voiceover script.
You have ACTUALLY READ this chapter using AI vision. The following is your detailed
chapter-by-chapter analysis — including dialogue, scenes, character moments, and plot points.

MANGA: {title}
AUTHOR: {author}

YOUR CHAPTER ANALYSIS (from actually reading the pages):
{chapter_analysis[:3000]}

REQUIREMENTS:
- STRICT word limit: 170-180 words MAX. No exceptions. Count carefully.
- Target length: ~{target_seconds} seconds of speech
- Style: {voice_vibe} — short, punchy, every sentence earns its place
- You MUST reference SPECIFIC scenes and dialogue quotes from the analysis
- Do NOT write a generic overview — discuss what ACTUALLY HAPPENS in this chapter
- Structure (tight):
  HOOK (1 punchy sentence)
  → PREMISE (2-3 sentences: what happens, stakes)
  → KEY MOMENTS (3-4 sentences: best scenes, dialogue quotes)
  → VERDICT (1-2 sentences: honest take + rating)
  → CTA: "Subscribe for more reviews"
- Write ONE continuous narration — no scene headers, no [image] tags
- NO filler words, NO rambling, NO "I think" / "In my opinion"
- Short sentences. Strong verbs. Punchy rhythm.
- You are reviewing THIS CHAPTER specifically, not the whole series

OUTPUT: Just the raw narration text. No markdown, no headers. 170-180 words."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1500,
        "temperature": 0.7,
    }

    print(f"[NARRATE] Generating {target_seconds}s review for '{title}' (VISION-INFORMED) via {model}...")
    r = requests.post(
        f"{base_url}/chat/completions",
        headers=headers,
        json=payload,
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()

    narration = data["choices"][0]["message"]["content"].strip()
    word_actual = len(narration.split())
    est_seconds = word_actual / 3

    print(f"[NARRATE] Done — {word_actual} words (~{est_seconds:.0f}s of speech)")
    return narration


def generate_narration_from_synopsis(metadata: dict, target_seconds: int = 60, voice_vibe: str = "analytical") -> str:
    """Legacy mode: generate narration from metadata/synopsis only (no vision analysis)."""
    api_key = os.environ.get("OPENCODE_GO_API_KEY")
    base_url = os.environ.get("OPENCODE_GO_BASE_URL", "https://opencode.ai/zen/go/v1")
    model = os.environ.get("OPENCODE_GO_MODEL", "hy3")

    if not api_key:
        print("[ERROR] OPENCODE_GO_API_KEY not set. Check .env or environment.")
        sys.exit(1)

    word_count = 175  # tight, punchy — every word earns its place
    title = metadata.get("title", "Unknown")
    author = metadata.get("author", "Unknown")
    synopsis = metadata.get("synopsis", "No synopsis available.")
    tags = ", ".join(metadata.get("tags", []))
    status = metadata.get("status", "unknown")

    prompt = f"""You are a manga/manhua/manhwa SHORT-FORM video reviewer writing a voiceover script.

MANGA DETAILS:
- Title: {title}
- Author: {author}
- Genre/Tags: {tags}
- Status: {status}
- Synopsis: {synopsis[:500]}

REQUIREMENTS:
- STRICT word limit: 170-180 words MAX. Count carefully.
- Target length: ~{target_seconds} seconds of speech
- Style: {voice_vibe} — short, punchy, every sentence earns its place
- Structure (tight):
  HOOK (1 punchy sentence)
  → PREMISE (2-3 sentences: what happens, stakes)
  → KEY SELLING POINTS (3-4 sentences: art, characters, unique hooks)
  → VERDICT (1-2 sentences: honest take + rating)
  → CTA: "Subscribe for more reviews"
- Write ONE continuous narration — no scene headers, no [image] tags
- NO filler words, NO rambling, NO "I think" / "In my opinion"
- Short sentences. Strong verbs. Punchy rhythm.
- Be honest about weaknesses too

OUTPUT: Just the raw narration text. No markdown, no headers. 170-180 words."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "temperature": 0.7,
    }

    print(f"[NARRATE] Generating {target_seconds}s review for '{title}' (SYNOPSIS-ONLY) via {model}...")
    r = requests.post(
        f"{base_url}/chat/completions",
        headers=headers,
        json=payload,
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()

    narration = data["choices"][0]["message"]["content"].strip()
    word_actual = len(narration.split())
    est_seconds = word_actual / 3

    print(f"[NARRATE] Done — {word_actual} words (~{est_seconds:.0f}s of speech)")
    return narration


def main():
    parser = argparse.ArgumentParser(description="Generate manga review narration")
    parser.add_argument("metadata", nargs="?", default=None, help="Path to metadata.json (legacy mode)")
    parser.add_argument("--summary", "-s", default=None, help="Path to chapter_summary.json (vision mode)")
    parser.add_argument("--output", "-o", default="narration.txt", help="Output narration file")
    parser.add_argument("--length", "-l", type=int, default=60, help="Target video length in seconds")
    parser.add_argument("--vibe", "-v", default="analytical", help="Voice vibe: analytical, hype, chill")
    args = parser.parse_args()

    load_env()

    # Determine mode: vision summary or legacy synopsis
    summary_path = args.summary
    if not summary_path:
        # Auto-detect: check for chapter_summary.json next to metadata
        if args.metadata:
            meta_dir = Path(args.metadata).parent
            auto_summary = meta_dir / "chapter_summary.json"
            if auto_summary.exists():
                summary_path = str(auto_summary)

    if summary_path and Path(summary_path).exists():
        print(f"[MODE] Vision-informed narration (using {summary_path})")
        with open(summary_path) as f:
            summary = json.load(f)
        narration = generate_narration_from_summary(summary, target_seconds=args.length, voice_vibe=args.vibe)
    elif args.metadata:
        print(f"[MODE] Synopsis-only narration (legacy fallback)")
        with open(args.metadata) as f:
            metadata = json.load(f)
        narration = generate_narration_from_synopsis(metadata, target_seconds=args.length, voice_vibe=args.vibe)
    else:
        print("[ERROR] Provide either metadata.json path or --summary chapter_summary.json")
        sys.exit(1)

    out_path = Path(args.output)
    out_path.write_text(narration)
    print(f"[SAVED] {out_path} ({len(narration)} chars)")


if __name__ == "__main__":
    main()
