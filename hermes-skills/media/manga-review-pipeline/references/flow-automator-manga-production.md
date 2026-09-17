# Flow Automator Max Production for Manga/Manhwa Video Pipeline

## Overview
This document specifies the end-to-end production pipeline connecting raw manga/manhwa chapters to Google Flow via the Flow Automator Max Chrome extension (`oogojcpkgjghajfnhcdlnfcnnkdenafh`).

## 1. The 5-Node Workflow (Excalidraw Architecture)

1. **Discovery & Input**: User inputs a manga/manhwa/manhua title or MangaDex URL.
2. **Source Material Resolution**:
   - Query MangaDex API (`/manga?title=...`).
   - If MangaDex has metadata but 0 hosted pages (common for licensed Kakao/Naver webtoons like *The Investor Who Sees The Future*), automatically fall back to webtoon reader scrapers (`theinvestorwhoseesthefuture.com`, `manhwatop.com`, etc.).
3. **Chapter Selection**: Ask user how many chapters to scrape (or accept `--chapters N`).
4. **Scraping**: Download full-resolution panels into `output/<slug>/ch<num>/images/` and save `metadata.json`.
5. **Agentic Processing Architecture**:
   - **CRITICAL RULE (Sequential Vision)**: Always use **ONE sequential image-analysis worker** for the chapter. Never parallelize page vision reading across multiple workers, as disjoint workers cause character names, chronology, tone, and dialogue interpretations to drift.
   - Run sequential analysis via `agy --model gemini-3.8-flash-medium --effort medium` (resumable per-page).
   - Save the canonical `chapter_analysis.json`.
   - **Downstream Fan-out (Safe Parallelism)**:
     - Worker 2: Generates detailed generative video animation prompts and `video_prompts.csv`.
     - Worker 3: Builds the 9:16 vertical SERYE drama block storyboards.
     - Both downstream workers consume the exact canonical JSON; they NEVER re-read images or reinterpret story beats independently.

## 2. Storyboard Format Contract (SERYE Drama Blocks)

- Storyboards must follow the SERYE 10-second drama block convention (e.g., 6 blocks × 10s = 60s total episode).
- Canvas: 9:16 vertical aspect ratio (768 × 1376 px).
- Layout: 5 horizontal tier rows (2 + 1 + 2 + 2 + 1 = 8 distinct visual shots / 6 timestamped beats):
  - Row 1: 2 panels side by side (`0s-1.5s` & `1.5s-3s`)
  - Row 2: 1 full-width panoramic panel (`3s-4.5s`)
  - Row 3: 2 panels side by side (`4.5s-6s`)
  - Row 4: 2 panels side by side (`6s-8s`)
  - Row 5: 1 full-width final panel (`8s-10s`)
- **Freeze Frame**: The final beat MUST explicitly end on `END ON A COMPLETE FREEZE FRAME: [Character] holds final pose motionless through 10s, zero extra movement.`
- **Irregular Durations**: If the final episode block cannot reach 10s (e.g. 6s), take note or state the exact duration explicitly.
- **Role of Storyboard**: The storyboard strip is a director's planning sheet. Do NOT feed the storyboard strip as an image ingredient to Google Flow.

## 3. Flow Automator Max V3 CSV Schema

The Chrome extension accepts CSV files with this exact 9-column header:
```csv
prompt,description,hashtags,videoModel,videoMode,videoDurationSeconds,flowQuantity,videoVoiceReference,flowAspectRatio
```

### Column Specifications:
- `prompt`: Multi-line prompt text starting with prepended `@CharacterName` mentions for React Fiber asset auto-binding.
- `description`: Scene identifier, e.g. `VIDEO: E01 B1 — The Question That Changes Everything`.
- `hashtags`: `#manhwa #investor #kdrama #drama #shortDrama #googleFlow`.
- `videoModel`: `Omni Flash`.
- `videoMode`: `ingredients`.
- `videoDurationSeconds`: `10`.
- `flowQuantity`: `1`.
- `videoVoiceReference`: Voice actor anchor / persona.
- `flowAspectRatio`: `9:16`.

## 4. Prompt Engineering to Neutralize Visual Storyboard Imperfections

When 2D AI-generated storyboard sheets have minor imperfections (duplicate poses, garbled UI text), prompt engineering compensates completely:
1. **Depth-of-Field Blurring for UI/Screens**: Specify shallow depth-of-field (85mm/100mm lens) with phone screens held at an angle displaying abstract glowing graphs in natural anamorphic bokeh, eliminating unreadable text artifacts.
2. **Distinct Focal Lengths for Split Panels**: Assign 24mm wide angle for establishing shots and 85mm prime lens for intimate character close-ups.
3. **Rigid Character Anchors**: Inject exact demographic, hair, eye, skin, and wardrobe descriptors matching character reference sheets to prevent facial morphing.
4. **Grounded Realism**: Strictly specify contemporary realistic setting details to block hallucinated fantasy elements or promotional banners.

## 5. Script Toolchain in `~/manga-reviews/`

- `manga_pipeline.py`: Master end-to-end CLI orchestrator.
- `manga_source_scraper.py`: MangaDex API + fallback web reader scraper.
- `sequential_chapter_analysis.py`: Canonical medium-effort sequential reader.
- `script_and_prompt_engine.py`: Subagents 1 & 2 script and video prompt generator.
- `build_serye_storyboard.py`: SERYE 10s drama block storyboard builder.
- `generate_nano_storyboards.py`: Character reference sheets & storyboard visual generator.
- `build_flow_automator_csv.py`: Flow Automator Max V3 production CSV exporter.
- Public GitHub repo: `https://github.com/koyawel0694/manga-video-pipeline`
