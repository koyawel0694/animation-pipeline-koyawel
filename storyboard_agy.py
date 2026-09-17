#!/usr/bin/env python3
"""
storyboard_agy.py — Subagent 3 (Storyboard 9:16 Video Generation Guide using Antigravity CLI).

Implements Node 5 (Subagent 3) & Final Deliverable Guide from Excalidraw:
- Analyzes the narrative flow of the story.
- Creates a 9:16 vertical video storyboard using `agy` (Google Antigravity CLI) as a video generation guide (ingredients).
- Outputs:
    1. storyboard_9_16.md  — Director's Markdown specification
    2. storyboard_9_16.html — Interactive dark-mode visual storyboard viewer with 9:16 frames
    3. storyboard_9_16.json — Machine-readable structured guide

Usage:
  python3 storyboard_agy.py --chapter-dir /home/john/manga-reviews/output/ch2
  python3 storyboard_agy.py --chapter-dir /home/john/manga-reviews/output/ch2 --max-scenes 5
"""

import os
import sys
import json
import csv
import time
import re
import argparse
import subprocess
from pathlib import Path
from typing import Optional

AGY_BIN = "/home/john/.local/bin/agy"


def call_agy(prompt: str, timeout: int = 90) -> str:
    """Invoke Google Antigravity CLI (agy) in headless mode."""
    cmd = [AGY_BIN, "-p", prompt]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if res.returncode != 0:
        raise RuntimeError(f"agy execution failed (code {res.returncode}): {res.stderr}")
    return res.stdout.strip()


def parse_agy_json(raw: str) -> dict:
    """Parse JSON returned by agy, stripping codeblocks if present."""
    text = raw.strip()
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"(\{.*\})", text, re.DOTALL)
        if m:
            return json.loads(m.group(1))
        raise


def build_beat_prompt(scene: dict, total_scenes: int) -> str:
    """Construct prompt for agy to design the 9:16 vertical storyboard beat."""
    return f"""You are an expert anime and short-form video director creating a 9:16 vertical video storyboard for TikTok, YouTube Shorts, and Reels.

Target Scene {scene.get('Scene_Number', 1)} of {total_scenes}:
- Speaker: {scene.get('Character_Speaker', 'Narrator')}
- Dialogue: {scene.get('Dialogue_Script', '')}
- Action: {scene.get('Action_Description', '')}
- Manga Panel: {scene.get('Page_File', 'panel.jpg')}
- Proposed Animation Prompt: {scene.get('Video_Animation_Prompt', '')}

Create the director's 9:16 vertical video beat with complete "Ingredients" needed to manually generate this video clip in AI video models (Google Flow, Kling, Runway, Luma).

Return ONLY valid JSON with no markdown backticks:
{{
  "beat_number": {scene.get('Scene_Number', 1)},
  "title": "Short punchy title for this cut",
  "duration_sec": {scene.get('Estimated_Duration_Sec', 4.0)},
  "vertical_composition_9_16": "Detailed framing guide for 9:16 vertical screen: what sits in the top UI safe zone (upper 15%), center primary action zone (middle 70%), and bottom subtitle safe zone (lower 15%). Explain how the manga art is cropped or expanded.",
  "ingredients": {{
    "source_panel": "{scene.get('Page_File', 'panel.jpg')}",
    "character_visual_anchor": "Precise character appearance cues (costume, hair, eyes, skin tone, signature props) to maintain character consistency across cuts",
    "environment_plate": "Background setting, architecture, lighting color temperature, atmospheric VFX (e.g. particles, dust motes, haze)",
    "camera_motion_cue": "Specific camera kinematics (e.g. low-angle tilt, 1.2x slow push-in, lateral dolly pan, subtle handheld breathing)",
    "audio_dialogue": "{scene.get('Dialogue_Script', '')}",
    "audio_sfx": "Exact sound effects to layer (e.g. heavy bell strike, metal sword clash, echoing footsteps)",
    "audio_bgm": "Musical cue, tempo, instruments, and emotional mood"
  }},
  "manual_generation_recipe": "1-2 sentence quick recipe for the user when entering this into video generators"
}}
"""


def generate_storyboard_agy(
    chapter_dir: Path,
    output_dir: Optional[Path] = None,
    max_scenes: Optional[int] = None,
) -> tuple[list[dict], Path, Path]:
    """
    Subagent 3: Runs Antigravity CLI analysis over chapter scenes and builds
    the 9:16 vertical storyboard guide (Markdown + HTML).
    """
    chapter_dir = chapter_dir.resolve()
    if output_dir is None:
        output_dir = chapter_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load scenes from pipeline_data.json or video_prompts.csv
    csv_path = chapter_dir / "video_prompts.csv"
    json_data_path = chapter_dir / "pipeline_data.json"
    scenes = []

    if json_data_path.exists():
        with open(json_data_path, "r", encoding="utf-8") as f:
            jdata = json.load(f)
            scenes = jdata.get("scenes", [])
            # Map keys to match CSV format
            for sc in scenes:
                sc["Scene_Number"] = sc.get("scene_number")
                sc["Character_Speaker"] = sc.get("speaker")
                sc["Dialogue_Script"] = sc.get("full_tts_script") or sc.get("dialogue_text")
                sc["Action_Description"] = sc.get("action_description")
                sc["Video_Animation_Prompt"] = sc.get("video_animation_prompt")
                sc["Page_File"] = sc.get("page_file")
                sc["Estimated_Duration_Sec"] = sc.get("estimated_duration_sec", 4.0)

    elif csv_path.exists():
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            scenes = list(reader)

    if not scenes:
        raise RuntimeError(f"No scene data found in {chapter_dir}. Run script_and_prompt_engine.py first.")

    if max_scenes and max_scenes > 0:
        scenes = scenes[:max_scenes]

    print(f"\n{'='*60}")
    print(f"  SUBAGENT 3: 9:16 STORYBOARD & INGREDIENTS GUIDE (via Antigravity agy)")
    print(f"  Processing {len(scenes)} scenes...")
    print(f"{'='*60}")

    storyboard_beats = []
    for idx, sc in enumerate(scenes, start=1):
        print(f"\n[AGY STORYBOARD] Beat {idx}/{len(scenes)}: {sc.get('Character_Speaker', 'Narrator')}...")
        prompt = build_beat_prompt(sc, len(scenes))
        try:
            raw_res = call_agy(prompt)
            beat_data = parse_agy_json(raw_res)
            # Ensure panel image path is stored
            beat_data["panel_file"] = sc.get("Page_File")
            storyboard_beats.append(beat_data)
            print(f"  -> Created beat: '{beat_data.get('title')}' ({beat_data.get('duration_sec')}s)")
        except Exception as e:
            print(f"  [WARN] agy call failed for beat {idx}: {e}")
            # Fallback beat
            storyboard_beats.append({
                "beat_number": idx,
                "title": f"Scene {idx}",
                "duration_sec": float(sc.get("Estimated_Duration_Sec", 4.0)),
                "vertical_composition_9_16": "Center action focused on 9:16 frame with top/bottom safe zones for mobile playback.",
                "panel_file": sc.get("Page_File"),
                "ingredients": {
                    "source_panel": sc.get("Page_File"),
                    "character_visual_anchor": sc.get("Character_Speaker", "Protagonist"),
                    "environment_plate": "Detailed fantasy background matching panel setting",
                    "camera_motion_cue": "Slow push-in, 9:16 framing",
                    "audio_dialogue": sc.get("Dialogue_Script", ""),
                    "audio_sfx": "Ambient room tone and scene Foley",
                    "audio_bgm": "Atmospheric dramatic underscore",
                },
                "manual_generation_recipe": "Load panel into Kling/Flow, set 9:16, prompt camera push-in.",
            })

    # 2. Generate storyboard_9_16.md
    md_path = output_dir / "storyboard_9_16.md"
    total_duration = sum(b.get("duration_sec", 4.0) for b in storyboard_beats)

    md_lines = [
        f"# 9:16 Vertical Video Storyboard & Generation Guide",
        f"**Target Format:** 9:16 Vertical (1080x1920) for TikTok / Reels / Shorts",
        f"**Total Cuts:** {len(storyboard_beats)} shots",
        f"**Estimated Runtime:** ~{total_duration:.1f} seconds",
        f"**Generated by:** Google Antigravity CLI (`agy`) Subagent 3",
        "",
        "---",
        "",
    ]

    for b in storyboard_beats:
        bnum = b.get("beat_number", 1)
        btitle = b.get("title", "")
        bdur = b.get("duration_sec", 4.0)
        ing = b.get("ingredients", {})

        md_lines.extend([
            f"## Cut #{bnum}: {btitle} ({bdur}s)",
            f"- **Source Panel Image:** `{b.get('panel_file')}`",
            f"- **9:16 Framing & Safe Zones:** {b.get('vertical_composition_9_16')}",
            f"",
            f"### 📋 Ingredients Breakdown",
            f"- **👤 Character Visual Anchor:** {ing.get('character_visual_anchor')}",
            f"- **🏰 Environment & Lighting Plate:** {ing.get('environment_plate')}",
            f"- **🎥 Camera & Motion Cue:** {ing.get('camera_motion_cue')}",
            f"- **🎙️ Dialogue & VO Script:** `{ing.get('audio_dialogue')}`",
            f"- **🔊 Sound Effects (SFX):** {ing.get('audio_sfx')}",
            f"- **🎵 Music & Mood (BGM):** {ing.get('audio_bgm')}",
            f"",
            f"**⚡ Manual Generation Recipe:** {b.get('manual_generation_recipe')}",
            "",
            "---",
            "",
        ])

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # 3. Generate interactive HTML viewer (storyboard_9_16.html)
    html_path = output_dir / "storyboard_9_16.html"
    html_content = generate_html_viewer(storyboard_beats, total_duration, chapter_dir)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 4. Save structured JSON
    json_path = output_dir / "storyboard_9_16.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_cuts": len(storyboard_beats),
            "total_duration_sec": total_duration,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "beats": storyboard_beats,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n[COMPLETE] Subagent 3 produced 9:16 Storyboard materials:")
    print(f"  - Markdown Guide: {md_path}")
    print(f"  - Visual HTML:    {html_path}")
    print(f"  - Structured JSON:{json_path}")
    return storyboard_beats, md_path, html_path


def generate_html_viewer(beats: list[dict], total_duration: float, chapter_dir: Path) -> str:
    """Generate standalone dark-themed 9:16 visual storyboard viewer."""
    cards_html = []
    for b in beats:
        bnum = b.get("beat_number", 1)
        btitle = b.get("title", "")
        bdur = b.get("duration_sec", 4.0)
        panel_file = b.get("panel_file", "")
        ing = b.get("ingredients", {})
        recipe = b.get("manual_generation_recipe", "")
        framing = b.get("vertical_composition_9_16", "")

        # Image relative path check
        img_rel = f"images/{panel_file}"

        cards_html.append(f"""
        <div class="beat-card">
          <div class="beat-header">
            <div class="cut-badge">CUT #{bnum}</div>
            <div class="cut-title">{btitle}</div>
            <div class="cut-duration">⏱️ {bdur}s</div>
          </div>

          <div class="beat-body">
            <!-- 9:16 Phone Mockup -->
            <div class="phone-mockup-wrapper">
              <div class="phone-frame">
                <div class="phone-notch"></div>
                <div class="safe-zone top-zone">TOP SAFE ZONE (UI)</div>
                <div class="phone-content">
                  <img src="{img_rel}" alt="{panel_file}" onerror="this.parentElement.innerHTML='<div class=img-fallback>Panel: {panel_file}</div>'">
                </div>
                <div class="safe-zone bottom-zone">BOTTOM CAPTION ZONE</div>
              </div>
              <div class="panel-tag">Source: <code>{panel_file}</code></div>
            </div>

            <!-- Ingredients & Instructions -->
            <div class="ingredients-content">
              <div class="section-title">📐 9:16 Composition & Safe Zones</div>
              <div class="framing-desc">{framing}</div>

              <div class="section-title">🧪 Ingredients For Generation</div>
              <div class="grid-ingredients">
                <div class="ing-item">
                  <span class="ing-label">👤 Character Anchor:</span>
                  <span class="ing-val">{ing.get('character_visual_anchor', '')}</span>
                </div>
                <div class="ing-item">
                  <span class="ing-label">🏰 Environment Plate:</span>
                  <span class="ing-val">{ing.get('environment_plate', '')}</span>
                </div>
                <div class="ing-item">
                  <span class="ing-label">🎥 Camera Cue:</span>
                  <span class="ing-val highlight-cam">{ing.get('camera_motion_cue', '')}</span>
                </div>
                <div class="ing-item">
                  <span class="ing-label">🎙️ Dialogue / VO:</span>
                  <span class="ing-val highlight-dial">{ing.get('audio_dialogue', '')}</span>
                </div>
                <div class="ing-item">
                  <span class="ing-label">🔊 SFX Cue:</span>
                  <span class="ing-val">{ing.get('audio_sfx', '')}</span>
                </div>
                <div class="ing-item">
                  <span class="ing-label">🎵 BGM Mood:</span>
                  <span class="ing-val">{ing.get('audio_bgm', '')}</span>
                </div>
              </div>

              <div class="recipe-box">
                <span class="recipe-icon">⚡</span>
                <div>
                  <strong>Quick Recipe:</strong> {recipe}
                </div>
              </div>
            </div>
          </div>
        </div>
        """)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>9:16 Manga Video Storyboard — Subagent 3 Guide</title>
  <style>
    :root {{
      --bg: #0d1117;
      --card-bg: #161b22;
      --border: #30363d;
      --text: #c9d1d9;
      --accent: #58a6ff;
      --accent-cyan: #39c5bb;
      --accent-magenta: #ff4785;
      --accent-yellow: #f1e05a;
    }}
    body {{
      margin: 0;
      padding: 24px;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    header {{
      background: linear-gradient(135deg, #1f2937, #111827);
      padding: 24px 32px;
      border-radius: 12px;
      border: 1px solid var(--border);
      margin-bottom: 30px;
    }}
    h1 {{
      margin: 0 0 8px 0;
      font-size: 26px;
      color: #fff;
    }}
    .subtitle {{
      color: #8b949e;
      font-size: 14px;
    }}
    .stats-bar {{
      display: flex;
      gap: 20px;
      margin-top: 16px;
      font-size: 13px;
    }}
    .stat-badge {{
      background: #21262d;
      padding: 6px 12px;
      border-radius: 6px;
      border: 1px solid var(--border);
    }}
    .beat-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      margin-bottom: 24px;
      overflow: hidden;
    }}
    .beat-header {{
      background: #1c2128;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      border-bottom: 1px solid var(--border);
    }}
    .cut-badge {{
      background: var(--accent);
      color: #000;
      font-weight: 800;
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 4px;
      letter-spacing: 0.5px;
    }}
    .cut-title {{
      font-size: 16px;
      font-weight: 600;
      color: #fff;
      flex: 1;
    }}
    .cut-duration {{
      font-size: 13px;
      color: #8b949e;
    }}
    .beat-body {{
      display: flex;
      flex-direction: row;
      gap: 24px;
      padding: 20px;
    }}
    @media (max-width: 860px) {{
      .beat-body {{ flex-direction: column; }}
    }}
    .phone-mockup-wrapper {{
      width: 220px;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .phone-frame {{
      width: 200px;
      height: 355px; /* 9:16 aspect */
      background: #000;
      border: 3px solid #484f58;
      border-radius: 28px;
      overflow: hidden;
      position: relative;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
      display: flex;
      flex-direction: column;
    }}
    .phone-notch {{
      width: 60px;
      height: 8px;
      background: #484f58;
      border-radius: 0 0 8px 8px;
      margin: 0 auto;
      z-index: 10;
    }}
    .phone-content {{
      flex: 1;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #1a1a1a;
    }}
    .phone-content img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    .img-fallback {{
      padding: 10px;
      color: #8b949e;
      font-size: 11px;
      text-align: center;
    }}
    .safe-zone {{
      position: absolute;
      left: 0;
      right: 0;
      font-size: 9px;
      font-weight: 700;
      text-align: center;
      letter-spacing: 0.5px;
      padding: 4px 0;
      pointer-events: none;
      z-index: 5;
    }}
    .top-zone {{
      top: 10px;
      background: rgba(255, 71, 133, 0.4);
      color: #ffb3cc;
      border-bottom: 1px dashed #ff4785;
    }}
    .bottom-zone {{
      bottom: 0;
      height: 48px;
      background: rgba(57, 197, 187, 0.35);
      color: #b3fff8;
      border-top: 1px dashed #39c5bb;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .panel-tag {{
      margin-top: 10px;
      font-size: 11px;
      color: #8b949e;
    }}
    .ingredients-content {{
      flex: 1;
    }}
    .section-title {{
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #8b949e;
      margin-bottom: 8px;
    }}
    .framing-desc {{
      font-size: 13px;
      line-height: 1.5;
      background: #0d1117;
      padding: 10px 14px;
      border-radius: 6px;
      border: 1px solid #21262d;
      margin-bottom: 16px;
    }}
    .grid-ingredients {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 16px;
    }}
    @media (max-width: 600px) {{
      .grid-ingredients {{ grid-template-columns: 1fr; }}
    }}
    .ing-item {{
      background: #0d1117;
      border: 1px solid #21262d;
      padding: 10px 12px;
      border-radius: 6px;
      font-size: 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .ing-label {{
      font-weight: 700;
      color: #8b949e;
    }}
    .ing-val {{
      color: #e6edf3;
      line-height: 1.4;
    }}
    .highlight-cam {{
      color: var(--accent-cyan);
      font-weight: 600;
    }}
    .highlight-dial {{
      color: var(--accent-yellow);
      font-style: italic;
    }}
    .recipe-box {{
      background: #1f2a37;
      border-left: 4px solid var(--accent);
      padding: 12px 16px;
      border-radius: 0 6px 6px 0;
      font-size: 13px;
      display: flex;
      gap: 10px;
      align-items: center;
    }}
    .recipe-icon {{
      font-size: 18px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>🎬 9:16 Vertical Video Storyboard & Ingredients Guide</h1>
      <div class="subtitle">Designed for manual generation on Google Flow / Kling / Runway / Luma</div>
      <div class="stats-bar">
        <div class="stat-badge">Total Cuts: <strong>{len(beats)}</strong></div>
        <div class="stat-badge">Total Est. Runtime: <strong>~{total_duration:.1f}s</strong></div>
        <div class="stat-badge">Aspect Ratio: <strong>9:16 Vertical (1080x1920)</strong></div>
        <div class="stat-badge">Engine: <strong>Google Antigravity CLI (agy)</strong></div>
      </div>
    </header>

    {"".join(cards_html)}
  </div>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Subagent 3 Storyboard & Ingredients Guide via Antigravity")
    parser.add_argument("--chapter-dir", "-d", required=True, help="Path to chapter output directory")
    parser.add_argument("--output-dir", "-o", default=None, help="Output directory (default: same as chapter-dir)")
    parser.add_argument("--max-scenes", "-m", type=int, default=None, help="Max scenes to storyboard")
    args = parser.parse_args()

    ch_dir = Path(args.chapter_dir)
    out_dir = Path(args.output_dir) if args.output_dir else ch_dir
    generate_storyboard_agy(ch_dir, output_dir=out_dir, max_scenes=args.max_scenes)


if __name__ == "__main__":
    main()
