---
name: animation-pipeline-koyawel
description: "Use when running the animation-pipeline-koyawel manga/manhwa/webtoon-to-video asset pipeline."
version: 1.0.0
author: John, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [animation, manga, manhwa, webtoon, storyboards, block-prompts, video]
    category: media
    related_skills: [manga-video-storyboard-pipeline, manga-review-pipeline, ai-drama-series-pipeline]
---

# Animation Pipeline Koyawel

Production-grade automated asset pipeline converting manga, manhwa, manhua, and webtoons into short-form vertical video assets (TikTok, YouTube Shorts, Reels, Google Flow, Kling).

## Repository & Environment

- Working checkout: `/home/john/animation-pipeline-koyawel/`
- Python environment: Python 3.12 (`~/.venv_manga` or system Python 3)
- Style configuration: `style_presets.json`
- Verification script: `verify_manga_chapter_assets.py`
- Test suite: `python3 -m unittest discover -s tests`

## Core Asset Deliverables

1. **Scraped chapter panels**: Clean, numbered pages in `output/<slug>/ch<N>/images/` plus `metadata.json` and canonical `chapter_analysis.json`.
2. **Character reference model sheets**: 9:16 PNG turnarounds (`768x1376`) on neutral studio backdrops in `character_refs/`.
3. **9:16 vertical storyboards**: 10-second SERYE drama director sheets (`768x1376`, 5 rows: 2+1+2+2+1, 6 beats with timestamps, ending on freeze frame) in `nano_storyboards/`.
4. **Block prompts only in .txt format**: Plain-text Flow/Kling prompt files (`blockN_prompts.txt` with `@@@NEXT@@@` delimiter, `blockN_video_prompt.txt`, and `flow_6_continuous_blocks.txt`) in `flow_queue/`.

## Multi-Style Support

Supported presets configured in `style_presets.json`:
- `photorealistic_live_action` — live-action cinematic adaptation (real human performers, cinematic lighting/lenses, practical/CGI effects).
- `webtoon_2d` — authentic Korean webtoon manhwa line art, flat cel-shaded coloring, controlled 2D animation.
- `anime_sakuga_2d` — high-energy hand-drawn key poses, dynamic perspective, impact frames, speed effects.
- `motion_comic_2d` — source-faithful art with multiplane parallax, pans/zooms, and selective movement.

To select a style preset for export:
```bash
python3 build_block_prompts_txt.py --chapter-dir output/<slug>/ch<N> --style-preset photorealistic_live_action
```

## Canonical Pipeline Stages

### Stage 1: Scrape Chapter Panels
```bash
python3 manga_source_scraper.py --url "<MANGA_URL>" --output-dir output/<slug>/ch<N>
```

### Stage 2: Canonical Sequential Chapter Analysis
```bash
python3 sequential_chapter_analysis.py --chapter-dir output/<slug>/ch<N>
```

### Stage 3: Character Reference Sheets
```bash
python3 generate_nano_storyboards.py --chapter-dir output/<slug>/ch<N> --reference-dir output/<slug>/ch1/character_refs
```

### Stage 4: 9:16 Vertical Storyboards
```bash
python3 build_serye_storyboard.py --analysis output/<slug>/ch<N>/chapter_analysis.json --output-dir output/<slug>/ch<N>
python3 compose_chapter_storyboards.py --chapter-dir output/<slug>/ch<N> --reference-dir output/<slug>/ch1/character_refs
```

### Stage 5: Block Prompts (.txt format with @@@NEXT@@@)
```bash
python3 build_block_prompts_txt.py --chapter-dir output/<slug>/ch<N> --style-preset <PRESET>
```

### Stage 6: Asset Verification
```bash
python3 verify_manga_chapter_assets.py output/<slug>/ch<N>
```
