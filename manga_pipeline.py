#!/usr/bin/env python3
"""
manga_pipeline.py — Master Orchestrator for Manga/Manhua/Manhwa Video Pipeline.

End-to-End Production Pipeline:
  [Stage 1: Source Discovery & Scraper]
      - Finds manga on MangaDex API or webtoon reader fallback
      - Interactive / CLI chapter selection ("How many chapters to scrape?")
      - Downloads all pages/panels cleanly into output/<manga>/ch<num>/images/
      ↓
  [Stage 2: Canonical Sequential Image Analysis]
      - Single sequential reader using Google Antigravity CLI (agy --effort medium)
      - Maintains strict chronological story continuity across all pages
      - Exports canonical `chapter_analysis.json`
      ↓
  [Stage 3: Downstream Video & Storyboard Specialization]
      ├─ Subagent 1 & 2: Scene-level dialogue script + video prompts -> video_prompts.csv
      ├─ Subagent 3: 10-second SERYE Drama Storyboard Blocks (6 beats per block, timestamps, freeze frame)
      ├─ Character Ref Sheets: 9:16 multi-view model sheets via Nano Banana Pro
      └─ Block prompt TXT package (one plain-text file per storyboard block)
      ↓
  [Stage 4: Optional downstream video generation]
      - Use clean single-frame crops or character refs as ingredients when requested

Usage:
  Interactive:
    python3 manga_pipeline.py
  CLI Full End-to-End:
    python3 manga_pipeline.py --title "The Investor Who Sees The Future" --chapters 1
  Run on existing scraped chapter:
    python3 manga_pipeline.py --existing-dir ./output/the-investor-who-sees-the-future/ch1
  Run specific stages only:
    python3 manga_pipeline.py --existing-dir ./output/the-investor-who-sees-the-future/ch1 --stage flow
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from manga_source_scraper import run_pipeline_source_flow


def print_banner(text: str):
    line = "=" * 68
    print(f"\n{line}")
    print(f"  {text}")
    print(f"{line}\n")


def run_command(cmd: list[str], label: str):
    print(f"[RUNNING] {label}...")
    t0 = time.time()
    res = subprocess.run(cmd, cwd=str(SCRIPT_DIR), text=True)
    dt = time.time() - t0
    if res.returncode != 0:
        print(f"[FAILED] {label} (exit code {res.returncode})")
        sys.exit(res.returncode)
    print(f"[OK] {label} finished in {dt:.1f}s\n")


def resolve_character_reference_dir(chapter_dir: Path) -> Path:
    """Reuse sibling Chapter 1 character refs for later chapters."""
    chapter_dir = chapter_dir.resolve()
    chapter_one = chapter_dir.parent / "ch1" / "character_refs"
    if chapter_one.is_dir():
        return chapter_one
    return chapter_dir / "character_refs"


def visual_generation_command(
    chapter_dir: Path,
    python_bin: str,
    reference_dir: Path | None = None,
) -> list[str]:
    """Return legacy Nano command using shared character refs."""
    reference_dir = reference_dir or resolve_character_reference_dir(chapter_dir)
    return [
        python_bin,
        str(SCRIPT_DIR / "generate_nano_storyboards.py"),
        "--chapter-dir",
        str(chapter_dir),
        "--reference-dir",
        str(reference_dir),
        "--all",
    ]


def storyboard_asset_command(
    chapter_dir: Path,
    python_bin: str,
    reference_dir: Path | None = None,
) -> list[str]:
    """Return deterministic storyboard-sheet compositor command."""
    reference_dir = reference_dir or resolve_character_reference_dir(chapter_dir)
    return [
        python_bin,
        str(SCRIPT_DIR / "compose_chapter_storyboards.py"),
        "--chapter-dir",
        str(chapter_dir),
        "--reference-dir",
        str(reference_dir),
    ]


def character_generation_command(chapter_dir: Path, python_bin: str, style_preset: str | None = None) -> list[str]:
    """Return first-chapter character-reference generation command."""
    cmd = [
        python_bin,
        str(SCRIPT_DIR / "generate_nano_storyboards.py"),
        "--chapter-dir",
        str(chapter_dir),
        "--characters",
    ]
    if style_preset:
        cmd.extend(["--style-preset", style_preset])
    return cmd


def choose_style_preset(chapter_dir: Path | None = None, requested_preset: str | None = None) -> str:
    """Prompt or resolve art style preset before generating assets."""
    config_path = SCRIPT_DIR / "style_presets.json"
    if not config_path.exists():
        return requested_preset or "webtoon_2d"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    presets = config.get("presets", {})

    if requested_preset:
        if requested_preset in presets:
            return requested_preset
        available = ", ".join(sorted(presets))
        raise ValueError(f"Unknown style preset {requested_preset!r}; choose one of: {available}")

    if chapter_dir:
        sel = chapter_dir / "style_selection.json"
        if sel.exists():
            try:
                val = json.loads(sel.read_text()).get("default_preset")
                if val in presets:
                    return val
            except Exception:
                pass

    if sys.stdin and sys.stdin.isatty():
        print("\n" + "=" * 60)
        print(" SELECT ART & ANIMATION STYLE PRESET BEFORE GENERATION")
        print("=" * 60)
        preset_keys = list(presets.keys())
        for idx, key in enumerate(preset_keys, 1):
            label = presets[key].get("label", key)
            desc = presets[key].get("description", "")
            print(f"  [{idx}] {label} ({key})")
            if desc:
                print(f"      {desc}")
        print("=" * 60)
        try:
            choice = input(f"Enter choice [1-{len(preset_keys)}] (default: 1): ").strip()
            if not choice:
                return preset_keys[0]
            if choice.isdigit() and 1 <= int(choice) <= len(preset_keys):
                return preset_keys[int(choice) - 1]
            elif choice in presets:
                return choice
        except (EOFError, KeyboardInterrupt):
            pass

    available = ", ".join(sorted(presets))
    raise RuntimeError(
        f"No art/animation style preset selected and no style_selection.json found in {chapter_dir}.\n"
        f"Specify --style-preset <name>. Available presets: {available}"
    )


def run_character_assets(chapter_dir: Path, python_bin: str, style_preset: str | None = None):
    """Ensure identity character references exist."""
    refs = resolve_character_reference_dir(chapter_dir)
    if not refs.is_dir() or not list(refs.glob("*.png")):
        run_command(
            character_generation_command(chapter_dir, python_bin, style_preset=style_preset),
            label="Initial Character Reference Generator",
        )


def run_storyboard_assets(chapter_dir: Path, python_bin: str, style_preset: str | None = None):
    """Ensure identity refs exist, then build chapter storyboard PNGs."""
    run_character_assets(chapter_dir, python_bin, style_preset=style_preset)
    refs = resolve_character_reference_dir(chapter_dir)
    run_command(
        storyboard_asset_command(chapter_dir, python_bin, refs),
        label="Character-Referenced Storyboard Sheet Composer",
    )


def orchestrate_manga_pipeline(
    title_or_url: str = None,
    num_chapters: int = None,
    max_pages_per_ch: int = None,
    existing_dir: str = None,
    stage: str = "all",
    output_base: str | None = None,
    style_preset: str | None = None,
    episodes: int | None = None,
    pages_per_episode: int = 22,
) -> list[Path]:
    base_out = Path(output_base or (SCRIPT_DIR / "output")).resolve()
    base_out.mkdir(parents=True, exist_ok=True)
    python_bin = sys.executable

    target_chapter_dirs = []

    # Step 1: Resolve target chapter directories
    if existing_dir:
        ed = Path(existing_dir).resolve()
        if not ed.exists():
            raise FileNotFoundError(f"Existing directory not found: {ed}")
        target_chapter_dirs.append(ed)
        print_banner(f"USING EXISTING CHAPTER DIRECTORY: {ed.name}")
    else:
        print_banner("STAGE 1: SOURCE DISCOVERY & CHAPTER SCRAPING")
        scraped_metas = run_pipeline_source_flow(
            input_target=title_or_url,
            num_chapters=num_chapters,
            output_base=base_out,
            max_pages_per_ch=max_pages_per_ch,
        )

        if not scraped_metas:
            print("[ABORT] No chapters were downloaded or selected.")
            return []

        for meta in scraped_metas:
            ch_num = meta["chapter"]["chapter"]
            images = meta.get("images", [])
            if images:
                ch_dir = Path(images[0]).parent.parent
            else:
                manga_slug = meta.get("title", "manga").lower().replace(" ", "-")
                ch_dir = base_out / manga_slug / f"ch{ch_num}"
            target_chapter_dirs.append(ch_dir)

    # Process each chapter
    for ch_dir in target_chapter_dirs:
        print_banner(f"PROCESSING CHAPTER: {ch_dir.name}")
        ch_dir = ch_dir.resolve()

        # Step 0: Resolve Art Style Preset before any generation
        active_style = choose_style_preset(ch_dir, requested_preset=style_preset)
        selection_path = ch_dir / "style_selection.json"
        if style_preset or not selection_path.exists():
            config_path = SCRIPT_DIR / "style_presets.json"
            preset_label = active_style
            if config_path.exists():
                presets = json.loads(config_path.read_text(encoding="utf-8")).get("presets") or {}
                preset_label = presets.get(active_style, {}).get("label", active_style)
            selection_path.write_text(json.dumps({
                "default_preset": active_style,
                "label": preset_label,
                "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }, indent=2), encoding="utf-8")
        print(f"[STYLE] Active art style preset: {active_style}\n")

        # Stage: Canonical Sequential Image Analysis
        if stage in ("all", "analyze"):
            print_banner("STAGE 2: CANONICAL SEQUENTIAL IMAGE ANALYSIS")
            analysis_script = SCRIPT_DIR / "sequential_chapter_analysis.py"
            run_command(
                [python_bin, str(analysis_script), "--chapter-dir", str(ch_dir)],
                label="Sequential Canonical Analysis (agy --effort medium)",
            )

        # Stage: Scene-Level Prompts & Dialogue CSV
        if stage in ("all", "prompts"):
            print_banner("STAGE 3A: SCENE PROMPTS & DIALOGUE EXTRACTION")
            prompts_script = SCRIPT_DIR / "script_and_prompt_engine.py"
            csv_path = ch_dir / "video_prompts.csv"
            run_command(
                [python_bin, str(prompts_script), "--chapter-dir", str(ch_dir), "--output-csv", str(csv_path)],
                label="Subagent 1 & 2 Scene Engine",
            )

        # Stage: 10-Second SERYE Drama Storyboard Blocks (Episodic)
        if stage in ("all", "storyboard", "visuals"):
            print_banner("STAGE 3B: 10-SECOND SERYE DRAMA STORYBOARD BLOCKS (EPISODIC)")
            serye_script = SCRIPT_DIR / "build_serye_storyboard.py"
            canon_json = ch_dir / "chapter_analysis.json"
            if canon_json.exists():
                serye_cmd = [
                    python_bin,
                    str(serye_script),
                    "--analysis",
                    str(canon_json),
                    "--output-dir",
                    str(ch_dir),
                ]
                if episodes:
                    serye_cmd.extend(["--episodes", str(episodes)])
                elif pages_per_episode:
                    serye_cmd.extend(["--pages-per-episode", str(pages_per_episode)])
                run_command(
                    serye_cmd,
                    label="SERYE Multi-Part Storyboard Blocks Builder",
                )
            else:
                print(f"[WARN] Missing {canon_json}; skipping storyboard block definition.")

        # Stage: Character identity refs (standard in all pipeline runs)
        if stage in ("all", "characters", "refs"):
            print_banner("STAGE 3C: CHARACTER REFS")
            run_character_assets(ch_dir, python_bin, style_preset=active_style)

        # Stage: Optional visual storyboard PNG sheets (opt-in only via --stage storyboard-sheets)
        if stage in ("storyboard-sheets", "visuals"):
            print_banner("STAGE 3C-OPT: STORYBOARD PNG SHEETS")
            storyboard_json = ch_dir / "storyboard_9_16.json"
            if storyboard_json.exists():
                refs = resolve_character_reference_dir(ch_dir)
                run_command(
                    storyboard_asset_command(ch_dir, python_bin, refs),
                    label="Character-Referenced Storyboard Sheet Composer",
                )

        # Stage: plain-text block prompts
        if stage in ("all", "flow"):
            print_banner("STAGE 3D: BLOCK PROMPTS (PLAIN TEXT)")
            prompt_txt_script = SCRIPT_DIR / "build_block_prompts_txt.py"
            run_command(
                [python_bin, str(prompt_txt_script), "--chapter-dir", str(ch_dir), "--style-preset", active_style],
                label="Chapter Block Prompt TXT Exporter",
            )

        # Print Final Deliverables Summary for Chapter
        print_banner("CHAPTER PRODUCTION DELIVERABLES READY")
        print(f"Target Directory: {ch_dir}\n")
        print("Key Artifacts Generated:")
        print(f"1. Canonical Story Analysis:     {ch_dir / 'chapter_analysis.json'}")
        print(f"2. Scene-Level Video Prompts:    {ch_dir / 'video_prompts.csv'}")
        print(f"3. SERYE 10s Storyboard Markdown: {ch_dir / 'storyboard_9_16.md'}")
        print(f"4. SERYE 10s Storyboard HTML:     {ch_dir / 'storyboard_9_16.html'}")
        print(f"5. Character Reference Sheets:   {ch_dir / 'character_refs'}")
        print(f"6. Block Prompt TXT Files:       {ch_dir / 'flow_queue'}")
        print("-" * 68)

    print_banner("PIPELINE COMPLETE — CHAPTER ASSET PACK READY")
    return target_chapter_dirs


def main():
    parser = argparse.ArgumentParser(description="Master Manga Video Pipeline Orchestrator")
    parser.add_argument("--title", "-t", default=None, help="Manga title to search")
    parser.add_argument("--url", "-u", default=None, help="Manga URL to scrape")
    parser.add_argument("--chapters", "-c", type=int, default=None, help="How many chapters to scrape")
    parser.add_argument("--max-pages", "-m", type=int, default=None, help="Max pages per chapter")
    parser.add_argument("--existing-dir", "-e", default=None, help="Process an existing chapter directory")
    parser.add_argument("--stage", default="all", choices=["all", "scrape", "analyze", "prompts", "storyboard", "visuals", "flow"], help="Run specific pipeline stage")
    parser.add_argument("--output-base", "-o", default=None, help="Output base directory (defaults to ./output)")
    parser.add_argument("--style-preset", "-s", default=None, help="Art style preset (e.g. photorealistic_live_action, studio_ghibli, webtoon_2d, etc.)")
    parser.add_argument("--episodes", type=int, default=None, help="Override number of 60s episodes for long chapters")
    parser.add_argument("--pages-per-episode", type=int, default=22, help="Target pages per 60s episode (default: 22)")
    args = parser.parse_args()

    target = args.url or args.title
    orchestrate_manga_pipeline(
        title_or_url=target,
        num_chapters=args.chapters,
        max_pages_per_ch=args.max_pages,
        existing_dir=args.existing_dir,
        stage=args.stage,
        output_base=args.output_base,
        style_preset=args.style_preset,
        episodes=args.episodes,
        pages_per_episode=args.pages_per_episode,
    )


if __name__ == "__main__":
    main()
