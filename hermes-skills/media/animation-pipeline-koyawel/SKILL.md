---
name: animation-pipeline-koyawel
description: "Use when running the animation-pipeline-koyawel manga/manhwa/webtoon-to-video asset pipeline."
version: 1.2.0
author: John, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [manga, manhwa, scraping, character-refs, storyboards, block-prompts, video]
    category: media
    related_skills: [ai-drama-series-pipeline, ai-video-content-qa, serye-web]
---

# Animation Pipeline Koyawel

Turns one scraped manga/manhwa/manhua chapter into production-ready short-form video assets:
1. **Scraped chapter panels**: Clean, numbered narrative pages in `output/<slug>/ch<N>/images/` plus `metadata.json` and canonical `chapter_analysis.json`.
2. **Character reference model sheets**: 9:16 PNG turnarounds (`768x1376`) in `character_refs/` on neutral studio backdrops (`#F4F4F4`) with front full-body, 3/4 portrait, side profile, and action pose **matching the chosen art/animation style preset** (e.g. photorealistic live-action real human actors when `photorealistic_live_action` is selected; 2D model sheets when `webtoon_2d` is selected). Never paste 2D comic panels into a live-action reference.
3. **10-second SERYE drama storyboard blocks**: 6-beat blocks with timestamps and freeze-frame ending in `storyboard_9_16.json`, `storyboard_9_16.md`, and `storyboard_9_16.html`. Visual PNG storyboard sheet compositing (legacy `nano_storyboards/`) is omitted from default deliverables.
4. **Block prompts in .txt format**: Plain-text Flow/Kling prompt files (`blockN_prompts.txt` with `@@@NEXT@@@` delimiter and `blockN_video_prompt.txt`) in `flow_queue/`.

Visual storyboard PNG sheet generation (`nano_storyboards/` and `clean_frame_crops/`) is REMOVED from default pipeline deliverables. Video generation tools take prompt text and clean character references, not composite collage sheets. No final video rendering, no narration audio generation, no review prose, and no CSV files required.

## When to Use

- Scrape manga/manhwa/manhua panels from a URL or title into clean chapter assets.
- Generate or reuse series character model sheets (9:16 PNGs at `768x1376`) matching the selected style preset.
- Build 10-second SERYE drama narrative storyboard blocks (6 beats with timestamps, ending on freeze frame) in `storyboard_9_16.json`.
- Export shot-by-shot and continuous block prompts in plain `.txt` format with `@@@NEXT@@@`.
- Verify a chapter's visual assets against the production contract.

Don't use for: video rendering, audio/TTS synthesis, or CSV queue generation (plain `.txt` format is the deliverable).

## Prerequisites

- Working directory: `/home/john/manga-reviews/` (or `/home/john/animation-pipeline-koyawel/`)
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
  style_selection.json
  character_refs/
    <character_slug>_ref.png              # 768x1376 9:16 PNG model sheets matching style preset
  character_refs_source.json              # Provenance manifest (reused for Ch2+)
  storyboard_9_16.json                    # Canonical storyboard metadata (6 beats/block)
  storyboard_9_16.md / .html              # Production documentation
  flow_queue/
    block1_prompts.txt                    # 6 shots separated by @@@NEXT@@@
    block1_video_prompt.txt               # Continuous 10s master block prompt
    ...
    flow_6_continuous_blocks.txt          # All blocks combined with @@@NEXT@@@
    flow_all_36_shots.txt                 # Flat shots combined
    prompt_txt_manifest.json              # Manifest of all text prompts
```

## End-to-End Execution Workflow

### Stage 0: Mandatory Art & Animation Style Selection (Prompt User First)

**CRITICAL AGENT RULE**:
Before generating ANY visual assets (character reference model sheets or block prompts), you **MUST** ask the user to choose their preferred art and animation style using the `clarify` tool, UNLESS they already explicitly specified it in their prompt!

**STRICT RULE**:
- NEVER silently default to 2D manhwa or any other style.
- NEVER assume or default based on previous sessions, memory profile notes, or other series.
- Fabricating `selected_by_user: true` in `style_selection.json` without asking the user via `clarify` is strictly forbidden.
- Always confirm the user's preferred style before generating character references or prompts.

Present the choices via `clarify`:
1. "Cinematic Photorealistic Live-Action (real human actors, grounded sets, cinematic lighting)"
2. "2D Korean Webtoon / Manhwa Anime (crisp ink line art, flat cel shading, manhwa anatomy)"
3. "Studio Ghibli Nostalgic Hand-Painted Anime (watercolor backgrounds, soft natural cel shading)"
4. "Dynamic Anime Sakuga Action (high-energy hand-drawn key poses, impact frames, speed lines)"
*(Additional presets in `style_presets.json`: Stylized 3D Animated Film, Dark Fantasy Anime, Motion Comic, Cyberpunk Neon, Classic Comic Book).*

Save choice to `output/<slug>/ch<N>/style_selection.json` and pass `--style-preset <PRESET>` to `build_block_prompts_txt.py` and `manga_pipeline.py`.

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
python3 sequential_chapter_analysis.py --chapter-dir output/<slug>/ch<N> --effort medium
```
Output: `chapter_analysis.json` containing exact dialogue, parenthesized vocal emotion tags `(emotion, tone)`, scene action, camera movement, and visual FX.

### Stage 3: Character Reference Model Sheets Matching Selected Style
- For Chapter 1 (or Ch 0): Create 9:16 vertical PNG model sheets (`768x1376`) for recurring characters:
  ```bash
  python3 generate_nano_storyboards.py --chapter-dir output/<slug>/ch1 --characters --style-preset <SELECTED_PRESET>
  ```
  - **Style Preset Enforcement**: The generated sheet MUST match the selected art style!
    - When `photorealistic_live_action` is selected: Model sheets MUST portray real human actors with visible skin pores, natural hair strands, physically tailored costumes, 85mm portrait lens on a neutral off-white studio backdrop (`#F4F4F4`), with 4 consistent turnaround views (front full-body, 3/4 portrait, side profile, dynamic action pose). NEVER paste 2D comic panels into a live-action reference sheet!
    - When `webtoon_2d` or `anime_sakuga_2d` is selected: Use authentic 2D anime/webtoon turnaround art.
- For Chapter 2+: **Reuse Chapter 1 character references** to preserve visual identity across the series:
  ```bash
  python3 generate_nano_storyboards.py --chapter-dir output/<slug>/ch<N> --reference-dir output/<slug>/ch1/character_refs
  ```
  Writes `character_refs_source.json` pointing to Chapter 1 without duplicate files.

### Stage 4: Storyboard Narrative Blocks (storyboard_9_16.json)
Build 10-second SERYE drama storyboard blocks (6 timing beats per block, timestamps, dialogue, ending on freeze frame):
- For short chapters (<= 25 pages), 1 standard 60-second episode is generated (6 blocks = 60s total).
- For long chapters (> 25 pages, e.g. 50-70 pages), the generator automatically segments the chapter into **multi-part 60s episodes** (~20-22 pages per episode) to prevent cramming:
```bash
python3 build_serye_storyboard.py --analysis output/<slug>/ch<N>/chapter_analysis.json --output-dir output/<slug>/ch<N> --pages-per-episode 22
```
Output: `storyboard_9_16.json`, `storyboard_9_16.md`, and `storyboard_9_16.html`.
*NOTE: Visual storyboard sheet compositing (`nano_storyboards/*.png` and `clean_frame_crops/`) is REMOVED from the default pipeline. The narrative storyboard JSON feeds directly into prompt generation.*

### Stage 5: Block Prompts Only in .txt Format
Export plain-text prompts for video generators (Google Flow, Kling, Runway):
```bash
python3 build_block_prompts_txt.py --chapter-dir output/<slug>/ch<N> --style-preset <SELECTED_PRESET>
```
Output: `flow_queue/block[1-6]_prompts.txt` (each containing 6 shot prompts separated by `\n\n@@@NEXT@@@\n\n`), `block[1-6]_video_prompt.txt`, and `flow_6_continuous_blocks.txt`.
- Style lock: Follows the selected preset from Stage 0 (e.g. Photorealistic Live-Action, 2D Korean Webtoon, Studio Ghibli, etc.) via `style_presets.json`. Prompt directives use `style_anchor`, `motion_anchor`, and `negative_anchor`.
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
4. **No Visual Storyboard Sheets**: Do NOT generate `nano_storyboards/*.png` or `clean_frame_crops/`. The deliverable is `storyboard_9_16.json` which feeds prompt generation.
5. **No Scanlation Watermarks**: Exclude all promotional inserts, scanlator credits, and aggregator logos from narrative pages.
6. **Style Preset Fidelity**: Character references and block prompts must strictly adhere to the chosen art/animation style preset. When `photorealistic_live_action` is chosen, character references must depict real human actors with natural skin texture and physical costumes—NEVER paste 2D comic art or crops into live-action reference sheets.
7. **Parenthesized Emotion Tags**: Dialogue emotion cues must be inside parentheses at the start of the quote `(emotion, tone) Dialogue...`.
