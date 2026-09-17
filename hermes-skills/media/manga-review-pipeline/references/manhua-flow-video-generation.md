# Manhua / Manhwa AI Video Generation & Flow Automator Workflow

## Core Lessons & Critical Rules (Sep 09 2026)

### 1. The Storyboard Is a Blueprint, NEVER a Video Input
- **The Pitfall**: Attaching a multi-panel storyboard sheet (with black dividing gutters, headers, and 6 comic panels) as an input image into Google Flow / Veo causes the model to literally animate the comic page itself (borders, timestamps, and multi-panel layout appearing inside the video).
- **The Rule**:
  - The 10-second SERYE storyboard sheet is strictly a **director's planning blueprint** for the human creator.
  - **NEVER attach the storyboard sheet as an image ingredient in Google Flow.**
  - Generate videos **frame by frame (shot by shot)**: each row in the CSV generates a single, clean, full-bleed 9:16 vertical scene without any borders, grids, or on-screen text.
  - If attaching an input image in Flow, attach either:
    1. A **clean isolated panel crop** from `clean_frame_crops/` (single panel, zero borders, zero text).
    2. The **character reference model sheet** from `character_refs/` (e.g. `kang_jin_hoo_ref.png`).

### 2. Enforcing 2D Manhwa / Webtoon Art Style (Preventing 3D CGI Drift)
- **The Pitfall**: Google Flow defaults to 3D CGI / photorealistic live-action humans if prompts use terms like "cinematic", "photorealistic", "skin pores", or lack explicit 2D cell-shading constraints.
- **The Rule**:
  - Every video prompt must lead with an enforced style directive:
    ```text
    Art style: authentic 2D Korean webtoon manhwa anime animation. Crisp clean dark ink line art, vibrant flat cel-shaded coloring, authentic manhwa character features, fluid 2D anime animation aesthetic. STRICTLY NOT 3D render, NOT live-action CGI, NOT photorealistic, NOT western comic book style. Full-bleed 9:16 vertical single continuous shot. Strictly NO comic panels, NO border frames, NO split screen, NO multi-panel collage, NO on-screen subtitles, NO speech bubbles, NO watermark.
    ```
  - Purge all photorealism trigger words ("skin pores", "4K film", "live action", "real camera crew").

### 3. Language Standard for Manhwa Productions: 100% English
- **The Pitfall**: Defaulting to Tagalog/Taglish based on local Philippine teleserye conventions (e.g. *Presiento* or *Hari ng Anino*).
- **The Rule**:
  - Manhwa and manhua video adaptations must default to **100% natural, crisp, cinematic English** for all dialogue scripts, voiceover cues, emotion tags, and prompt descriptions, unless explicitly directed otherwise by the user.

### 4. Sequential Single-Reader Analysis (No Parallel Vision Across Pages)
- **The Pitfall**: Spawning multiple subagents to analyze different page ranges in parallel causes narrative drift, inconsistent character names, disjointed timelines, and conflicting emotional tones.
- **The Rule**:
  - Use **one sequential reader worker** (`sequential_chapter_analysis.py`) running `agy --effort medium` for the entire chapter.
  - Produces a single, validated, canonical `chapter_analysis.json`.
  - Fan out downstream workers (prompts, storyboards, CSVs) in parallel ONLY AFTER the canonical analysis is saved, ensuring all downstream tools consume identical source data.

### 5. Flow Automator Max V3 Production CSV Schema
```csv
prompt,description,hashtags,videoModel,videoMode,videoDurationSeconds,flowQuantity,videoVoiceReference,flowAspectRatio
```
- Prepend `@CharacterName` (e.g. `@Kang Jin-Hoo`) so Flow Automator Max scans the React Fiber tree and automatically binds project character reference assets as Slate chip pills.
- Duration: Standard 5s, 8s, or 10s depending on mode.
- Final beat of every 10-second block must contain an explicit `END ON A COMPLETE FREEZE FRAME: [character] holds final pose motionless through 10s` instruction to prevent end-of-clip morphing.
