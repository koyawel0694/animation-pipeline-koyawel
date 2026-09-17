# animation-pipeline-koyawel

Production-grade automated AI animation and video production pipeline converting manga, manhwa, manhua, and webtoons into short-form vertical video assets (TikTok, YouTube Shorts, Reels, Google Flow, Kling).

This repository contains the complete pipeline toolset (formerly `manga-video-pipeline`), style presets, verification utilities, and bundled Hermes Agent skills.

---

## 🎬 Architecture & Workflow

```
[User Input: Manga Link or Title]
               │
               ▼
[Stage 1: Source Discovery & Chapter Scraper]
  ├─ MangaDex API Search & Title Resolution
  ├─ Webtoon Reader Fallback
  └─ Downloads panels into: output/<slug>/ch<num>/images/
               │
               ▼
[Stage 2: Canonical Sequential Image Analysis]
  └─ Single sequential reader via Google Antigravity CLI (agy --effort medium)
  └─ Preserves character names, chronology, exact dialogue, and story flow
  └─ Exports: output/<slug>/ch<num>/chapter_analysis.json
               │
               ▼
[Stage 3: Character References & Model Sheets]
  ├─ 9:16 Model Sheets on neutral studio backdrops (768x1376)
  ├─ Front full-body, 3/4 portrait, side profile, and action pose
  └─ Output: output/<slug>/ch<num>/character_refs/
               │
               ▼
[Stage 4: 9:16 Vertical Storyboards]
  ├─ 10-Second SERYE Drama Storyboard Blocks (5 rows: 2+1+2+2+1 = 8 shots)
  ├─ 6 timestamped beats per block ending on freeze frame
  └─ Output: output/<slug>/ch<num>/nano_storyboards/
               │
               ▼
[Stage 5: Block Prompts (.txt format with @@@NEXT@@@)]
  ├─ Plain-text Flow/Kling prompt files
  ├─ Multi-style presets (photorealistic live action, 2D webtoon, sakuga, motion comic)
  └─ Output: output/<slug>/ch<num>/flow_queue/
               │
               ▼
[Stage 6: Asset Verification]
  └─ verify_manga_chapter_assets.py validates chapter contract
```

---

## 🎨 Selectable Style Profiles

The pipeline supports configurable visual style presets via `style_presets.json`:

1. **`photorealistic_live_action`**: Live-action cinematic adaptation with real human performers, grounded sets, cinematic lenses, natural skin/lighting, and practical/CGI fantasy effects integrated into the live plate.
2. **`webtoon_2d`**: Authentic Korean webtoon manhwa anime animation with crisp clean dark ink lines, vibrant flat cel-shaded coloring, and controlled 2D animation.
3. **`anime_sakuga_2d`**: High-energy hand-drawn key poses, dynamic perspective, impact frames, speed effects, and expressive smears.
4. **`motion_comic_2d`**: Source-faithful artwork with multiplane parallax depth, camera pans, zooms, and selective movement.

### Selecting a Style

Pass `--style-preset` to `build_block_prompts_txt.py`:

```bash
python3 build_block_prompts_txt.py \
  --chapter-dir output/<slug>/ch<N> \
  --style-preset photorealistic_live_action
```

If a chapter contains `style_selection.json`, the exporter uses its `default_preset`. Otherwise it defaults to `webtoon_2d`.

---

## 👤 Character Consistency Rule

- **Chapter 0 / Chapter 1 Canonical Anchor**: The first chapter establishes canonical character reference model sheets.
- **Reusability**: Downstream chapters reuse existing character reference sheets to maintain visual identity across the entire series. Do not regenerate character references independently per chapter.
- **Cross-Style Translation**: When adapting from 2D comic art to live action, generate translated live-action actor/costume reference sheets rather than feeding 2D line art directly into photorealistic prompts.
- Recorded in `character_reference_policy.md` and `project_style_selection.json`.

---

## 🚀 Quick Start & CLI Usage

### 1. Scrape Chapter
```bash
python3 manga_source_scraper.py --url "<MANGA_URL>" --output-dir output/<slug>/ch1
```

### 2. Sequential Chapter Analysis
```bash
python3 sequential_chapter_analysis.py --chapter-dir output/<slug>/ch1
```

### 3. Generate Storyboard Metadata & Sheets
```bash
python3 build_serye_storyboard.py --analysis output/<slug>/ch1/chapter_analysis.json --output-dir output/<slug>/ch1
python3 compose_chapter_storyboards.py --chapter-dir output/<slug>/ch1 --reference-dir output/<slug>/ch1/character_refs
```

### 4. Build Block Prompts in Plain .txt Format
```bash
python3 build_block_prompts_txt.py --chapter-dir output/<slug>/ch1 --style-preset photorealistic_live_action
```

### 5. Verify Chapter Production Assets
```bash
python3 verify_manga_chapter_assets.py output/<slug>/ch1
```

---

## 🤖 Bundled Hermes Agent Skills

The repository bundles Hermes Agent skills under `hermes-skills/media/`:

- **`animation-pipeline-koyawel`**: End-to-end asset and prompt pipeline workflow for this repository.
- **`manga-video-storyboard-pipeline`**: Detailed operational specifications for panel scraping, character reference sheets, 9:16 vertical storyboards, and block prompt `.txt` generation.
- **`manga-review-pipeline`**: Production contract reference, slash command contracts, and downstream video/flow specifications.

---

## 🧪 Testing

Run the test suite:

```bash
python3 -m unittest discover -s tests
```

---

## 📄 License

MIT
