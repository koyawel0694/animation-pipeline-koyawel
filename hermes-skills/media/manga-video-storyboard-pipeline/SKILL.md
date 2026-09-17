---
name: manga-video-storyboard-pipeline
description: "Use when storyboarding manga chapters into video blocks."
version: 1.0.0
author: John, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [manga, manhwa, scraping, character-refs, storyboards, block-prompts, video]
    category: media
    related_skills: [ai-drama-series-pipeline, ai-video-content-qa, serye-web]
---

# Manga Video Storyboard Pipeline

Turns one scraped manga/manhwa/manhua chapter into production-ready short-form video assets:
1. **Scraped chapter panels**: Clean, numbered narrative pages in `output/<slug>/ch<N>/images/` plus `metadata.json` and canonical `chapter_analysis.json`.
2. **Character reference model sheets**: 9:16 PNG turnarounds (`768x1376`) on neutral studio backdrops (front full-body, 3/4 portrait, side profile, action pose) in `character_refs/`.
3. **10-second SERYE drama storyboard blocks**: 6-beat blocks with timestamps and freeze frame ending in `storyboard_9_16.json` (no visual PNG storyboard sheets).
4. **Block prompts in .txt format**: Plain-text Flow/Kling prompt files (`blockN_prompts.txt` with `@@@NEXT@@@` delimiter and `blockN_video_prompt.txt`) in `flow_queue/`.

Visual storyboard PNG sheet generation (legacy nano_storyboards/) is REMOVED from the pipeline. Video generation tools take prompt text, not composite storyboard sheets. No final video rendering, no narration audio generation, no review prose, and no CSV files required.

## When to Use

- Scrape manga/manhwa/manhua panels from a URL or title into clean chapter assets.
- Generate or reuse series character model sheets (9:16 PNGs) for visual consistency.
- Build 9:16 vertical 10-second drama storyboard sheets (5 rows: 2+1+2+2+1) from chapter scenes.
- Export shot-by-shot and continuous block prompts in plain `.txt` format with `@@@NEXT@@@`.
- Verify a chapter's visual assets against the production contract.

Don't use for: video rendering, audio/TTS synthesis, or CSV queue generation (plain `.txt` format is the deliverable).

## Prerequisites

- Working directory: `/home/john/manga-reviews/`
- Python virtualenv: `~/.venv_manga/` (Python 3.12 with PIL/Pillow, requests, bs4)
- Verification script: `/home/john/manga-reviews/verify_manga_chapter_assets.py`
- Test suite: `python3 -m unittest discover -s /home/john/manga-reviews/tests`

## Directory & Asset Structure

```text
output/<series-slug>/ch<chapter>/
  images/
    page_001.webp (or .png, .jpg)
    page_002.webp
    ...
  metadata.json
  chapter_analysis.json
  character_refs/
    <character_slug>_ref.png              # 768x1376 9:16 PNG model sheets
  character_refs_source.json              # Provenance manifest (reused for Ch2+)
  storyboard_9_16.json                    # Canonical storyboard metadata
  storyboard_9_16.md / .html              # Production documentation
  nano_storyboards/
    block01_<slug>.png                    # 768x1376 9:16 SERYE storyboard sheet
    block02_<slug>.png
    ...
  storyboard_assets_manifest.json
  flow_queue/
    block1_prompts.txt                    # 6 shots separated by @@@NEXT@@@
    block1_video_prompt.txt               # Continuous 10s master block prompt
    ...
    flow_6_continuous_blocks.txt          # All blocks combined with @@@NEXT@@@
    flow_all_36_shots.txt                 # Flat shots combined
    prompt_txt_manifest.json              # Manifest of all text prompts
```

Reference example on disk: `/home/john/manga-reviews/output/the-investor-who-sees-the-future/ch1/`.

## End-to-End Execution Workflow

### Stage 0: Mandatory Art & Animation Style Selection (Prompt User First)

**CRITICAL AGENT RULE**:
Before generating ANY visual assets (character reference model sheets, storyboards, or block prompts), you **MUST** ask the user to choose their preferred art and animation style using the `clarify` tool, UNLESS they already explicitly specified it in their prompt!

**STRICT RULE**:
- NEVER silently default to 2D manhwa or any other style.
- NEVER assume or default based on previous sessions, memory profile notes (e.g. 'Manga: 2D anime'), or other series.
- Fabricating `selected_by_user: true` in `style_selection.json` without asking the user via `clarify` is strictly forbidden.
- Never proceed to Stage 3 (Character Reference Model Sheets) or Stage 4 (Storyboards) without confirming the user's preferred style!

Present the choices via `clarify`:
1. "Cinematic Photorealistic Live-Action (real human actors, grounded sets, cinematic lighting)"
2. "Studio Ghibli Nostalgic Hand-Painted Anime (watercolor backgrounds, soft natural cel shading)"
3. "2D Korean Webtoon / Manhwa Anime (crisp ink line art, flat cel shading, manhwa anatomy)"
4. "Dynamic Anime Sakuga Action (high-energy hand-drawn key poses, impact frames, speed lines)"
5. "Stylized 3D Animated Film (Pixar/DreamWorks style 3D characters, tactile materials)"
6. "Dark Fantasy Anime (gritty chiaroscuro, heavy ink shadows, glowing magical auras)"

Save choice to `output/<slug>/ch<N>/style_selection.json` and pass `--style-preset <PRESET>` to `generate_nano_storyboards.py`, `build_block_prompts_txt.py`, and `manga_pipeline.py`.

### Stage 1: Scrape Chapter Panels
```bash
cd /home/john/manga-reviews
source ~/.venv_manga/bin/activate

# Discover and scrape via MangaDex API or webtoon mirrors:
python3 manga_source_scraper.py --query "<Manga Title>" --chapters 1

# Or download directly from chapter URL:
python3 scrape_manga.py "<Chapter URL>" --output-dir output/<slug>/ch<N>
```
Verify: Numbered pages in `output/<slug>/ch<N>/images/` must be 1-indexed and contiguous (`page_001`, `page_002`, ...). Strip any reader credit cards, advertisements, or scanlation recruitment inserts.

### Stage 2: Canonical Sequential Image Analysis
Always analyze pages sequentially in chronological order (never parallelize vision reading):
```bash
python3 sequential_chapter_analysis.py --chapter-dir output/<slug>/ch<N>
```
Output: `chapter_analysis.json` containing exact dialogue, parenthesized vocal emotion tags `(emotion, tone)`, scene action, camera movement, and visual FX.

### Stage 3: Character Reference Model Sheets (image-2.png)
- For Chapter 1: Create 9:16 vertical PNG model sheets (`768x1376`) for recurring characters:
  ```bash
  python3 generate_nano_storyboards.py --chapter-dir output/<slug>/ch1 --characters
  ```
  Each sheet features clean neutral studio backdrop (`#F4F4F4`), character name banner, front full-body view, 3/4 portrait, side profile, and casual/action pose.
- For Chapter 2+: **Reuse Chapter 1 character references** to preserve visual identity across the series:
  ```bash
  python3 generate_nano_storyboards.py --chapter-dir output/<slug>/ch<N> --reference-dir output/<slug>/ch1/character_refs
  ```
  Writes `character_refs_source.json` pointing to Chapter 1 without duplicate files.

### Stage 4: Storyboard Narrative Blocks (storyboard_9_16.json)
Build 10-second SERYE drama storyboard blocks (6 timing beats per block, timestamps, dialogue, ending on freeze frame):
```bash
python3 build_serye_storyboard.py --analysis output/<slug>/ch<N>/chapter_analysis.json --output-dir output/<slug>/ch<N>
```
Output: `storyboard_9_16.json` and `storyboard_9_16.md`.
NOTE: Visual storyboard sheet compositing (`compose_chapter_storyboards.py` -> `nano_storyboards/*.png`) is omitted. The JSON metadata feeds directly into the video prompt generator.

### Stage 5: Block Prompts Only in .txt Format (image-5.png)
Export plain-text prompts for video generators (Google Flow, Kling, Runway):
```bash
python3 build_block_prompts_txt.py --chapter-dir output/<slug>/ch<N>
```
Output: `flow_queue/block[1-6]_prompts.txt` (each containing 6 shot prompts separated by `\n\n@@@NEXT@@@\n\n`), `block[1-6]_video_prompt.txt`, and `flow_6_continuous_blocks.txt`.
- Style lock: Follows the selected preset from Stage 0 (e.g. 2D Korean webtoon, Anime Sakuga, Studio Ghibli, Dark Fantasy Anime, Photorealistic Live-Action, etc.) via style_presets.json. Prompt directives use style_anchor and motion_anchor.
- Dialogue: Spoken English lines with parenthesized emotion cues: `(energetic, broadcast tone) ...`
- Freeze frame: Beat 6 explicitly ends with: `Use the final beat as a complete freeze frame; do not add a new action after the final pose.`

### Stage 6: Verify Assets
Run the automated contract verifier:
```bash
python3 verify_manga_chapter_assets.py --chapter-dir output/<slug>/ch<N>
```
Must pass with exit code 0:
`[OK] output/<slug>/ch<N>: N pages, 6 blocks, 36 beats verified`

## Pitfalls & Core Rules

1. **TXT Format Only**: The user requires `.txt` files with `@@@NEXT@@@`. Do NOT generate or deliver CSV queues unless explicitly requested.
2. **Sequential Vision Only**: Never parallelize page analysis across multiple workers. Single sequential reader preserves chronology, character names, and dramatic tension.
3. **Reuse Character References**: Never regenerate character model sheets on later chapters; always link back to Chapter 1 references via `character_refs_source.json`.
4. **Storyboards Are Not Direct Inputs**: The 9:16 storyboard sheet (`image-4.png`) is a director overview guide containing panel borders and headers. Generative video tools take single-panel narrative crops or prompt text, not the combined sheet collage.
5. **No Scanlation Watermarks**: Exclude all promotional inserts, scanlator credits, and aggregator logos from narrative panels and storyboard crops.
6. **Strict 2D Aesthetic**: Every prompt locks 2D cel-shaded webtoon/anime animation; explicitly ban 3D CGI and photorealistic rendering.
7. **Parenthesized Emotion Tags**: Dialogue emotion cues must be inside parentheses at the start of the quote `(emotion, tone) Dialogue...`.
