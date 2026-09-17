---
name: animation-pipeline-koyawel
description: "Use when running the animation-pipeline-koyawel manga/manhwa/webtoon-to-video asset pipeline."
version: 1.1.0
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

---

## 🎨 Supported Art & Animation Styles

The pipeline supports 9 distinct visual presets in `style_presets.json`:

1. **`photorealistic_live_action`**: Cinematic Photorealistic Live-Action (real human actors, cinematic lenses, grounded sets, natural skin texture, practical/CGI fantasy VFX).
2. **`studio_ghibli`**: Studio Ghibli Nostalgic Hand-Painted Anime (lush watercolor backgrounds, soft natural cel shading, gentle expressive character linework, warm sunlight).
3. **`webtoon_2d`**: 2D Korean Webtoon / Manhwa Anime (crisp clean dark ink lines, vibrant flat cel shading, authentic manhwa character features, controlled fluid 2D animation).
4. **`anime_sakuga_2d`**: Dynamic Japanese Anime Sakuga Action (high-energy hand-drawn key poses, dynamic perspective distortion, sharp shadow cuts, impact frames, speed lines).
5. **`stylized_3d_animation`**: Stylized 3D Animated Film (Pixar / DreamWorks style, tactile materials, soft subsurface scattering on skin, dimensional studio lighting).
6. **`dark_fantasy_anime`**: Dark Fantasy Anime (gritty gothic chiaroscuro, heavy ink shadows, moody atmospheric haze, glowing magical aura effects).
7. **`cyberpunk_neon`**: Cyberpunk / Sci-Fi Anime (neon highlights, rain reflections, volumetric fog, chromatic aberration, sleek tech detailing).
8. **`motion_comic_2d`**: Source-Faithful Motion Comic (preserves original comic book / manhwa print artwork with multiplane parallax depth, camera pans, and zooms).
9. **`classic_comic_book`**: Western Graphic Novel / Comic Book (bold expressive ink brushstrokes, dynamic cross-hatching, vintage Ben-Day halftone dot styling).

---

## ⚠️ STAGE 0: MANDATORY STYLE PROMPT (BEFORE ALL PROCESSES)

**CRITICAL AGENT RULE**:
Before generating ANY visual assets (character reference model sheets, storyboards, or block prompts), you **MUST** prompt the user to choose their preferred art and animation style using the `clarify` tool, UNLESS the user has already explicitly stated their preferred style in their message!

**NEVER silently default to the 2D manhwa style or skip asking the user.**

When calling `clarify`, present the top recommended choices:
- "Cinematic Photorealistic Live-Action (real human actors, grounded sets, cinematic lighting)"
- "Studio Ghibli Nostalgic Hand-Painted Anime (watercolor backgrounds, soft natural cel shading)"
- "2D Korean Webtoon / Manhwa Anime (crisp ink line art, flat cel shading, manhwa anatomy)"
- "Dynamic Anime Sakuga Action (high-energy hand-drawn key poses, impact frames, speed lines)"
- "Stylized 3D Animated Film (Pixar/DreamWorks style 3D characters, tactile materials)"
- "Dark Fantasy Anime (gritty chiaroscuro, heavy ink shadows, glowing magical auras)"

Once the user selects a style:
1. Immediately save the selection to `output/<slug>/ch<N>/style_selection.json`:
   ```json
   {
     "default_preset": "<SELECTED_PRESET>",
     "label": "<LABEL>",
     "selected_by_user": true
   }
   ```
2. Pass `--style-preset <SELECTED_PRESET>` to ALL downstream generation commands.

---

## Canonical Pipeline Stages

### Stage 1: Scrape Chapter Panels
```bash
python3 manga_source_scraper.py --url "<MANGA_URL>" --output-dir output/<slug>/ch<N>
```

### Stage 2: Canonical Sequential Chapter Analysis
```bash
python3 sequential_chapter_analysis.py --chapter-dir output/<slug>/ch<N>
```

### Stage 3: Character Reference Sheets (In Selected Art Style)
Generate 9:16 model sheets matching the selected art style (e.g. photorealistic actor turnaround, Ghibli watercolor character, 2D webtoon, etc.):
```bash
python3 generate_nano_storyboards.py \
  --chapter-dir output/<slug>/ch<N> \
  --characters \
  --style-preset <SELECTED_PRESET>
```
*Note: For Chapter 2+, reuse established Chapter 1 references unless a style change was requested:*
```bash
python3 generate_nano_storyboards.py \
  --chapter-dir output/<slug>/ch<N> \
  --reference-dir output/<slug>/ch1/character_refs
```

### Stage 4: 9:16 Vertical Storyboards & Multi-Part Episodic Segmentation
For short chapters (<= 25 pages), 1 standard 60-second episode is generated (6 blocks of 10s).
For long chapters (> 25 pages, e.g. 50-70 pages), the generator automatically segments the chapter into **multi-part 60s episodes** (~20-22 pages per episode) to prevent cramming and narrative compression:
- Each episode has 6 blocks of 10s = 60s total, ending on a cliffhanger freeze-frame.
- Outputs are organized into `episodes/ep01/`, `ep02/`, `ep03/` with a master `episodes_manifest.json` and unified `storyboard_9_16.json`.
```bash
# Generate episodic storyboard metadata:
python3 build_serye_storyboard.py \
  --analysis output/<slug>/ch<N>/chapter_analysis.json \
  --output-dir output/<slug>/ch<N> \
  --pages-per-episode 22
```
*Note: Visual storyboard PNG sheets (legacy nano_storyboards/) are omitted. The narrative storyboard JSON feeds directly into prompt generation.*

### Stage 5: Block Prompts (.txt format with @@@NEXT@@@)
Export plain-text prompts for Google Flow, Kling, or Veo matching the selected style:
```bash
python3 build_block_prompts_txt.py \
  --chapter-dir output/<slug>/ch<N> \
  --style-preset <SELECTED_PRESET>
```

### Stage 6: Asset Verification
```bash
python3 verify_manga_chapter_assets.py output/<slug>/ch<N>
```
