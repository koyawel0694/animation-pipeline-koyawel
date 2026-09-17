# 9:16 Manga Video Storyboard & Animation Pipeline

GitHub Repository: `https://github.com/koyawel0694/manga-video-pipeline`
Location: `/home/john/manga-reviews/`
Venv: `~/.venv_manga/bin/python3`
Tools: Google Antigravity CLI (`/home/john/.local/bin/agy`), Vision Proxy (`http://localhost:8765/v1`)

## Full Architecture (Excalidraw Specification)

```
[User Input: Manga Link or Title]
               │
               ▼
[Manga Source Finder: MangaDex API / Web]
               │
               ▼
[Interactive Chapter Selection ("How many chapters to scrape?")]
               │
               ▼
[Manga Chapter Scraper: Download Panels & Metadata]
               │
               ├──► Subagent 1: Extract chat bubbles, analyze story flow,
               │                accurate character dialogue with VO emotion tags,
               │                detailed scene action descriptions
               │
               ├──► Subagent 2: Structured generative video animation prompts
               │                (camera kinematics, character dynamics, lighting, anime style)
               │
               └──► Subagent 3: 9:16 Vertical Storyboard & Ingredients Guide
                                (TikTok/Shorts safe zones, character visual anchors,
                                 camera cues, SFX/BGM audio cues via Google Antigravity CLI)
               │
               ▼
[Deliverables Generated]
 ├── video_prompts.csv   (Complete structured video prompts + character scripts)
 ├── storyboard_9_16.md  (Director-level 9:16 vertical production storyboard)
 ├── storyboard_9_16.html(Interactive dark-mode visual viewer with phone frames)
 └── pipeline_data.json  (Machine-readable structured dataset)
               │
               ▼
[Manual Video Generation by User]
 (Upload panel, paste prompt into Kling / Flow / Runway, generate TTS voiceover)
```

## Scripts

1. `manga_source_scraper.py`:
   - Searches MangaDex API (`/manga?title=...`) or resolves URLs.
   - Lists English chapters, deduplicates external redirect stubs.
   - Asks user how many chapters to scrape (interactive or `--chapters N`).
   - Downloads pages to `output/<slug>/ch<num>/images/page_XXX.jpg` + `metadata.json`.

2. `script_and_prompt_engine.py`:
   - Subagent 1: Queries vision proxy (`http://localhost:8765/v1`), extracts chat bubbles verbatim, character speaker, voice emotion cues inside parentheses `(flat, tired)` for TTS, and physical action descriptions.
   - Subagent 2: Generates detailed animation video prompts (subject motion, camera movement, lighting, anime cel-shading style).
   - Synthesizes into `video_prompts.csv` and `pipeline_data.json`.

3. `storyboard_agy.py`:
   - Invokes `/home/john/.local/bin/agy -p` (Google Antigravity CLI, Gemini 3.8 Flash).
   - Generates 9:16 vertical framing specs (top UI safe zone, center action zone, bottom caption safe zone).
   - Provides complete "Ingredients": Visual Anchor, Environment Plate, Camera Motion Cue, Audio SFX/BGM, and manual generation recipe.
   - Generates `storyboard_9_16.md` and `storyboard_9_16.html`.

4. `manga_pipeline.py`:
   - Master orchestrator connecting all steps end-to-end.

## Execution

```bash
# Full interactive run:
/home/john/.venv_manga/bin/python3 /home/john/manga-reviews/manga_pipeline.py

# Scrape and process 1 chapter by title:
/home/john/.venv_manga/bin/python3 /home/john/manga-reviews/manga_pipeline.py --title "From Goblin to Goblin God" --chapters 1

# Process already scraped chapter:
/home/john/.venv_manga/bin/python3 /home/john/manga-reviews/manga_pipeline.py --existing-dir /home/john/manga-reviews/output/ch2
```

## Workflow Pitfalls & Best Practices

- **Solo Flight Over Multi-Agent Delegation:** John prefers direct "solo flight" execution over spawning background subagents via `delegate_task` for this pipeline, ensuring fast iteration and immediate terminal feedback.
- **Parenthesized VO Emotion Tags:** Keep voiceover emotion cues inside parentheses at the start of dialogue lines (e.g. `(flat, tired) E-rank hunter ako...`) for seamless TTS intake.
- **Git Hygiene:** Do not track `.env`, `output/`, or raw downloaded image batches in git; `.gitignore` is configured to exclude images and binaries.
