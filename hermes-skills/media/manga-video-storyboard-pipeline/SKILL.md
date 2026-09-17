---
name: manga-video-storyboard-pipeline
description: "Use when storyboarding manga chapters into video blocks."
version: 1.4.0
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
2. **Canonical manga script ledger**: Exact non-empty source text in page/scene order, with stable scene IDs, speaker, delivery, text type, and source-analysis hash in `chapter_script.json`, `chapter_script.txt`, and `chapter_script.md`. Sound effects are explicitly marked as not spoken.
3. **Character reference model sheets**: 9:16 PNG turnarounds (`768x1376`) in `character_refs/` on neutral studio backdrops (`#F4F4F4`) with front full-body, 3/4 portrait, side profile, and action pose **matching the chosen art/animation style preset** (e.g. photorealistic live-action real human actors when `photorealistic_live_action` is selected; 2D model sheets when `webtoon_2d` is selected). Never paste 2D comic panels into a live-action reference.
4. **10-second SERYE drama storyboard blocks**: 6-beat blocks with timestamps and freeze-frame ending in `storyboard_9_16.json`, `storyboard_9_16.md`, and `storyboard_9_16.html`. For chapters > 25 pages, automatically segmented into 60s episodes (`episodes/ep01/`, `ep02/`). Visual PNG storyboard sheet compositing (legacy `nano_storyboards/`) is omitted from default deliverables.
5. **Block prompts in .txt format per block per episode**: Plain-text Flow/Kling prompt files (`blockN_prompts.txt` with `@@@NEXT@@@` delimiter and `blockN_video_prompt.txt`) in `flow_queue/` AND in each episode folder (`episodes/epXX/flow_queue/`), formatted for direct copy-paste into Google Flow. Both prompt forms carry the exact canonical script cue for every beat.

Visual storyboard PNG sheet generation (`nano_storyboards/` and `clean_frame_crops/`) is REMOVED from default pipeline deliverables. Video generation tools take prompt text and clean character references, not composite collage sheets. No final video rendering, no narration audio generation, no review prose, and no CSV files required.

## When to Use

- Scrape manga/manhwa/manhua panels from a URL or title into clean chapter assets.
- Generate or reuse series character model sheets (9:16 PNGs at `768x1376`) matching the selected style preset.
- Build 10-second SERYE drama narrative storyboard blocks (6 beats with timestamps, ending on freeze frame) in `storyboard_9_16.json`.
- Export shot-by-shot and continuous block prompts in plain `.txt` format with `@@@NEXT@@@` per block and per episode.
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
  chapter_script.json                  # exact source-text ledger; JSON is canonical
  chapter_script.txt / .md             # human-readable script exports
  style_selection.json
  character_refs/
    <character_slug>_ref.png              # 768x1376 9:16 PNG model sheets matching style preset
  character_refs_source.json              # Provenance manifest (reused for Ch2+)
  storyboard_9_16.json                    # Canonical storyboard metadata (6 beats/block)
  storyboard_9_16.md / .html              # Production documentation
  episodes_manifest.json                  # Multi-part episodic manifest (when > 25 pages)
  episodes/                               # Multi-part 60s episodic packages (when > 25 pages)
    ep01/
      storyboard_9_16.json / .md / .html
      chapter_script.json / .txt / .md
      flow_queue/
        block1_prompts.txt                # 6 shots separated by @@@NEXT@@@ (copy-paste ready)
        block1_video_prompt.txt           # Continuous 10s master block prompt
        ...
        block6_prompts.txt
        block6_video_prompt.txt
        flow_6_continuous_blocks.txt      # 6 continuous blocks for ep01
        flow_all_36_shots.txt             # 36 shots for ep01
        prompt_txt_manifest.json          # Manifest for ep01
    ep02/
      storyboard_9_16.json / .md / .html
      flow_queue/
        ...
  flow_queue/                             # Unified / single-episode prompt queue
    block1_prompts.txt                    # 6 shots separated by @@@NEXT@@@
    block1_video_prompt.txt               # Continuous 10s master block prompt
    ...
    flow_6_continuous_blocks.txt          # Continuous blocks separated by @@@NEXT@@@
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
Each scene must also carry `text_type` when known (`spoken`, `narration`, `thought`, `sfx`, `caption`, or `unknown`). Preserve `dialogue_text` exactly; classify sound effects as `sfx` so they are not sent to spoken TTS. Downstream stages generate `chapter_script.json`, `.txt`, and `.md` directly from this analysis—never from a second model pass.

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
Build 10-second SERYE drama storyboard blocks (6 timing beats per block, timestamps, exact script references, ending on freeze frame):
- For short chapters (<= 25 pages), 1 standard 60-second episode is generated (6 blocks = 60s total).
- For long chapters (> 25 pages, e.g. 50-70 pages), the generator automatically segments the chapter into **multi-part 60s episodes** (~20-22 pages per episode) to prevent cramming:
```bash
python3 build_serye_storyboard.py --analysis output/<slug>/ch<N>/chapter_analysis.json --output-dir output/<slug>/ch<N> --pages-per-episode 22
```
- **Webtoon Scroll Strips**: When a chapter is scraped as continuous vertical webtoon scroll strips (e.g. 8-12 tall images of ~13,000px height with 60-100+ scenes), the raw image count may be <= 25, but the narrative density equals a 60-80 page chapter. Always pass explicit `--episodes N` (e.g. `--episodes 3`) or `--pages-per-episode 3` so the story is properly divided into multiple 60s viral episodes instead of being crammed into a single 60s video.
Output: `chapter_script.json`, `chapter_script.txt`, `chapter_script.md`, `storyboard_9_16.json`, `storyboard_9_16.md`, and `storyboard_9_16.html`. Blocks are partitioned chronologically with non-overlapping source pools. If a block needs visual continuity beats, they are explicitly transitional and contain no repeated script line.
*NOTE: Visual storyboard sheet compositing (`nano_storyboards/*.png` and `clean_frame_crops/`) is REMOVED from the default pipeline. The narrative storyboard JSON feeds directly into prompt generation.*

### Stage 5: Block Prompts in .txt Format (Per Block & Per Episode)
Export plain-text prompts for video generators (Google Flow, Kling, Runway):
```bash
python3 build_block_prompts_txt.py --chapter-dir output/<slug>/ch<N> --style-preset <SELECTED_PRESET>
```
Output:
- **Per-Episode Flow Queues** (`episodes/ep01/flow_queue/`, `ep02/flow_queue/`):
  Each episode folder gets its own standalone `flow_queue/` with 1-indexed `block1_prompts.txt` through `block6_prompts.txt`, `block1_video_prompt.txt` through `block6_video_prompt.txt`, `flow_6_continuous_blocks.txt`, `flow_all_36_shots.txt`, and `prompt_txt_manifest.json`. Direct copy-paste ready for Google Flow!
- **Root Flow Queue** (`flow_queue/`):
  Full sequence of all blocks across all episodes (`block1_prompts.txt` to `blockN_prompts.txt`), combined continuous blocks, flat shots, and master manifest.
- Can also be invoked directly on an episode folder:
  ```bash
  python3 build_block_prompts_txt.py --chapter-dir output/<slug>/ch<N>/episodes/ep01
  ```
- Style lock: Follows the selected preset from Stage 0 (e.g. Photorealistic Live-Action, 2D Korean Webtoon, Studio Ghibli, etc.) via `style_presets.json`. Prompt directives use `style_anchor`, `motion_anchor`, and `negative_anchor`.
- Script fidelity: Every shot prompt and every `blockN_video_prompt.txt` continuous prompt must include the exact beat cue from the canonical ledger. Use `MANGA SCRIPT — Speaker: ... Exact line: "..."` for spoken/narrated text, `MANGA SOUND EFFECT (not spoken): ...` for SFX, and `MANGA SCRIPT: No spoken dialogue or voiceover for this beat. Do not invent dialogue.` for silent/transition beats. Never invent, paraphrase, repeat, or move dialogue between beats.
- Dialogue: Spoken English lines retain parenthesized emotion cues: `(energetic, broadcast tone) ...`; source text itself must not be rewritten.
- Freeze frame: Beat 6 explicitly ends with: `Use the final beat as a complete freeze frame; do not add a new action after the final pose.`

### Stage 6: Verify Assets
Run the automated contract verifier:
```bash
python3 verify_manga_chapter_assets.py --chapter-dir output/<slug>/ch<N>
```
Must pass with exit code 0:
`[OK] output/<slug>/ch<N>: N pages, M blocks, K beats verified with L source script lines` (verifies the source hash, script identity, scene references, non-overlapping episode ranges, root prompts, continuous prompts, and all episode queues).

## Pitfalls & Core Rules

1. **TXT Format Only**: The user requires `.txt` files with `@@@NEXT@@@`. Do NOT generate or deliver CSV queues unless explicitly requested.
2. **Prompts Per Episode**: For multi-part episodes, generate complete `flow_queue/` directories inside each `episodes/epXX/` folder so users can copy-paste blocks 1 to 6 directly into Google Flow without offset math.
3. **Sequential Vision Only**: Never parallelize page analysis across multiple workers. Single sequential reader preserves chronology, character names, and dramatic tension.
4. **Reuse Character References**: Never regenerate character model sheets on later chapters; always link back to Chapter 1 references via `character_refs_source.json`.
5. **No Visual Storyboard Sheets**: Do NOT generate `nano_storyboards/*.png` or `clean_frame_crops/`. The deliverable is `storyboard_9_16.json` which feeds prompt generation.
6. **No Scanlation Watermarks**: Exclude all promotional inserts, scanlator credits, and aggregator logos from narrative pages.
7. **Style Preset Fidelity**: Character references and block prompts must strictly adhere to the chosen art/animation style preset. When `photorealistic_live_action` is chosen, character references must depict real human actors with natural skin texture and physical costumes—NEVER paste 2D comic art or crops into live-action reference sheets.
8. **Parenthesized Emotion Tags**: Dialogue emotion cues must be inside parentheses at the start of the quote `(emotion, tone) Dialogue...`.
9. **Canonical Script Is Mandatory**: Never send a storyboard or prompt package downstream unless `chapter_script.json` matches `chapter_analysis.json` exactly. SFX is sound design, not spoken dialogue. A transition beat may reuse a visual anchor only when it has an explicit no-dialogue cue.
