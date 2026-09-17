# Character Reference Sheet Contract

This contract defines Stage 3 of the manga video storyboard pipeline: producing standardized character reference model sheets matching the selected art & animation style preset.

## 1. Purpose & Core Principles
Character reference sheets act as permanent identity anchors for the series. Generative video models (Google Flow, Kling, Runway, Veo) require consistent visual anchors across scenes. These reference sheets lock:
1. Facial geometry, eye shape and color, and hair style.
2. Exact silhouette, height, and anatomical proportions.
3. Wardrobe anchors (specific clothing items, colors, materials, and footwear).
4. Strict adherence to the active art & animation style preset (e.g. photorealistic live-action, 2D webtoon, Studio Ghibli, etc. from `style_presets.json`).

## 2. File Specifications
- **Directory**: `output/<series-slug>/ch<chapter>/character_refs/`
- **File Naming**: `<character_slug>_ref.png` (e.g. `han_jue_ref.png`, `fairy_xixuan_ref.png`, `kang_jin_hoo_ref.png`).
- **Format**: PNG image.
- **Dimensions**: Vertical portrait 9:16 aspect ratio (exactly `768x1376` pixels).
- **Background**: Solid neutral studio / model-sheet backdrop (`#F4F4F4` light off-white).

## 3. Layout Structure (Multi-Angle Model Sheet)
Each character sheet follows a standardized multi-angle model turnaround layout:
1. **Header Banner**: Clean, readable all-caps English character name banner at the top (e.g. `HAN JUE — LIVE ACTION REFERENCE`).
2. **Four Turnaround Views**:
   - **Front Full-Body View**: Standing posture from head to toe showing complete outfit, shoes, silhouette, and posture.
   - **3/4 Portrait Close-Up**: Detailed bust/headshot view showing facial contours, eye color, hair styling, and natural skin texture.
   - **Side Profile View**: True profile showing nose bridge, jawline, hair tie, and silhouette.
   - **Dynamic Action Pose**: Combat or casting pose demonstrating energy flow, martial stance, or spell channeling.

## 4. Art Style Lock & Preset Fidelity
Character reference sheets MUST strictly reflect the active style preset chosen in Stage 0:
- **`photorealistic_live_action`**: Must portray real human actors with natural skin pores, realistic hair strands, physically tailored garments with authentic fabric weave, photographed with an 85mm portrait cinema lens with soft key lighting. STRICTLY NOT 2D illustration, NOT anime drawing, NOT cel shaded. NEVER paste 2D comic crops into a photorealistic reference sheet.
- **`webtoon_2d`**: Authentic 2D Korean webtoon manhwa anime art with crisp ink line art, flat cel shading, and manhwa anatomy.
- **`studio_ghibli`**: Hand-painted aesthetic with watercolor texturing, soft natural cel shading, and gentle character linework.
- **`anime_sakuga_2d`**: Dynamic Japanese anime key art with sharp shadow cuts and impact poses.

## 5. Cross-Chapter Reuse Rule
- **Chapter 1 (or Ch 0) generates the canonical cast**: All recurring characters are generated once during the first chapter processing.
- **Subsequent chapters (Ch2+) REUSE Chapter 1**: Do NOT regenerate or duplicate character reference PNGs for recurring cast members in later chapters.
- **Provenance Manifest**: Later chapters point to the canonical reference directory via `character_refs_source.json`:
  ```json
  {
    "source_dir": "/path/to/output/<series-slug>/ch1/character_refs",
    "files": [
      ".../character_refs/han_jue_ref.png",
      ".../character_refs/fairy_xixuan_ref.png"
    ],
    "reused": true
  }
  ```
