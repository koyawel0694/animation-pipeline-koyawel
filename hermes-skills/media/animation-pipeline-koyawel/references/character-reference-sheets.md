# Character Reference Sheet Contract

This contract defines Stage 2 of the manga video storyboard pipeline: producing standardized character reference model sheets as shown in `/home/john/.codex/attachments/7f01f420-362f-4a66-8ac8-f0a7cc48fecc/image-2.png`.

## 1. Purpose & Core Principles
Character reference sheets act as permanent identity anchors for the series. AI video generators (such as Google Flow, Kling, or Runway) drift easily if given different visual cues per shot. These reference sheets lock:
1. Facial geometry, eye shape and color, and hair style.
2. Exact silhouette, height, and anatomical proportions.
3. Wardrobe anchors (specific clothing items, colors, and footwear).
4. Strict 2D Korean webtoon manhwa anime aesthetic (preventing unwanted 3D CGI or photorealism).

## 2. File Specifications
- **Directory**: `output/<series-slug>/ch1/character_refs/`
- **File Naming**: `<character_slug>_ref.png` (e.g., `kang_jin_hoo_ref.png`, `oh_taek_gyu_ref.png`, `street_reporter_ref.png`).
- **Format**: PNG image.
- **Dimensions**: Vertical portrait 9:16 aspect ratio (exactly `768x1376` pixels).
- **Background**: Solid neutral studio / model-sheet backdrop (`#F4F4F4` to `#F7F7F7` light gray/off-white). Never put characters on comic panels, speech bubbles, or busy backgrounds.

## 3. Layout Structure (Multi-Angle Model Sheet)
Each character sheet follows a standardized multi-angle model turnaround layout:
1. **Header Banner**: Clean, readable all-caps English character name banner at the top (e.g., `KANG JIN-HOO`, `OH TAEK-GYU`).
2. **Primary Full-Body Anchor (Left / Main View)**:
   - Full-body standing view from head to toe (front or 3/4 angle).
   - Shows complete outfit, shoes, silhouette, and posture.
3. **Portrait / Expression Close-Up (Upper Right)**:
   - Detailed bust/headshot view showing facial contours, eye reflections, hair texturing, and default emotional state.
4. **Side Profile & Action / Seated View (Lower Right)**:
   - True lateral side profile demonstrating jawline, nose bridge, and ear alignment.
   - Alternate pose (e.g., seated, holding signature prop, or mid-gesture).

## 4. Art Style Lock
Prompts generating or conditioning character reference sheets must strictly enforce:
```text
Art style: authentic 2D Korean webtoon manhwa anime animation. Crisp clean dark ink line art, vibrant flat cel-shaded coloring, authentic manhwa character features, fluid 2D animation. STRICTLY NOT 3D render, NOT live-action CGI, NOT photorealistic, NOT western comic-book style. Full-bleed 9:16 vertical single shot. NO comic panels, NO border frames, NO split screen, NO multi-panel collage, NO subtitles, NO speech bubbles, NO watermark.
```

## 5. Cross-Chapter Reuse Rule
- **Chapter 1 generates the canonical cast**: All recurring characters are generated during Chapter 1 processing.
- **Subsequent chapters (Ch2+) REUSE Chapter 1**: Do NOT regenerate or duplicate character reference PNGs for recurring cast members in later chapters.
- **Provenance Manifest**: Later chapters point to the canonical reference directory by recording:
  ```json
  // output/<series-slug>/ch2/character_refs_source.json
  {
    "source_dir": "/path/to/output/<series-slug>/ch1/character_refs",
    "files": [
      ".../character_refs/kang_jin_hoo_ref.png",
      ".../character_refs/oh_taek_gyu_ref.png"
    ],
    "reused": true
  }
  ```
