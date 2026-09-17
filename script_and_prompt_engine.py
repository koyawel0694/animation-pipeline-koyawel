#!/usr/bin/env python3
"""
script_and_prompt_engine.py — Subagent 1 (Dialogue/Script) & Subagent 2 (Video Animation Prompts) + CSV Synthesis.

Implements Nodes 5 & 6 from Excalidraw diagram:
- Subagent 1: Extracts chat bubbles, analyzes story flow, produces accurate script with granular action descriptions.
- Subagent 2: Creates detailed, structured generative video prompts that animate manga panels.
- CSV Engine: Synthesizes Subagent 1 + Subagent 2 outputs into a unified production CSV.

Usage:
  python3 script_and_prompt_engine.py --chapter-dir /home/john/manga-reviews/output/ch2 --max-pages 10
  python3 script_and_prompt_engine.py --chapter-dir /home/john/manga-reviews/output/ch2 --output-csv video_prompts.csv
"""

import os
import sys
import json
import csv
import base64
import time
import re
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

VISION_PROXY_URL = os.environ.get("VISION_PROXY_URL", "http://localhost:8765/v1")
VISION_MODEL = os.environ.get("VISION_MODEL", "antigravity")
VISION_TIMEOUT = int(os.environ.get("VISION_TIMEOUT", "120"))


def load_image_b64(path: str) -> str:
    """Read an image file and return base64 string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def call_vision_ai(images_b64: list[str], prompt: str, max_tokens: int = 3500) -> str:
    """Send image(s) and prompt to the local vision proxy backed by agy / Gemini."""
    content = [{"type": "text", "text": prompt}]
    for b64 in images_b64:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
        })

    payload = json.dumps({
        "model": VISION_MODEL,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{VISION_PROXY_URL}/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=VISION_TIMEOUT) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            if attempt == 2:
                raise RuntimeError(f"Vision proxy call failed after 3 attempts: {e}")
            time.sleep(2 * (attempt + 1))


def clean_json_response(raw_text: str) -> dict:
    """Extract and parse JSON from LLM/Vision output."""
    raw_text = raw_text.strip()
    # Strip markdown code blocks
    if "```json" in raw_text:
        raw_text = raw_text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in raw_text:
        raw_text = raw_text.split("```", 1)[1].split("```", 1)[0].strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback regex extraction of outermost JSON object
        m = re.search(r"(\{.*\})", raw_text, re.DOTALL)
        if m:
            return json.loads(m.group(1))
        raise


# ---------------------------------------------------------------------------
# SUBAGENT 1 + 2 DUAL EXTRACTION PROMPT
# ---------------------------------------------------------------------------

DUAL_EXTRACTION_PROMPT = """You are acting as two specialized subagents analyzing this manga/manhua page:

SUBAGENT 1 (Script & Dialogue Extractor):
1. Extract ALL text inside chat bubbles and narration boxes accurately and verbatim.
2. Identify the character speaking (use their name, role, or 'Narrator').
3. Supply a voice acting emotion cue INSIDE parentheses at the start of the dialogue, e.g. "(flat, tired)", "(shocked, eyes wide)", "(furious, gritting teeth)".
4. Detail the precise scene action description: character blocking, physical gestures, facial expressions, and camera framing.

SUBAGENT 2 (Structured Video Animation Prompt Generator):
For each scene / major panel on this page, create a production-ready generative video prompt that will animate this 2D manga panel into fluid motion (for Kling, Runway Gen-3, Google Flow, or Luma).
Every video prompt must include:
- Visual Subject & Action: Character appearance, dynamic movement, facial animation, hair/clothing dynamics.
- Cinematic Camera Movement: Specific motion (e.g., "slow dramatic push-in on eyes", "low-angle vertical tilt", "tracking shot").
- Lighting & Atmosphere: Cinematic lighting (chiaroscuro, volumetric haze, neon glow, embers, dark fantasy tint).
- Style & Aesthetics: "Cinematic anime animation, fluid motion, maintaining original manga line-art details".
- Estimated Duration: Suggested clip length in seconds (typically 3-6s).

Output STRICT VALID JSON with no additional commentary:
{
  "scenes": [
    {
      "scene_title": "Short descriptive title of scene",
      "panel_location": "top / center / bottom / full-page",
      "speaker": "Character Name or Narrator",
      "voice_emotion": "(emotion, tone)",
      "dialogue_text": "Verbatim chat bubble text (or narration)",
      "action_description": "Precise visual action and physical movement occurring in this panel",
      "video_animation_prompt": "Ultra-detailed prompt to animate this panel with subject, motion, camera, lighting, and style",
      "camera_movement": "Specific camera movement description",
      "visual_style_fx": "Lighting, atmosphere, and special effects",
      "estimated_duration_sec": 4.0
    }
  ]
}
"""


def process_page(image_path: Path, page_num: int, chapter_num: str) -> list[dict]:
    """Process a single page image through Subagent 1 & 2."""
    b64 = load_image_b64(str(image_path))
    prompt = f"Page {page_num} of Chapter {chapter_num}.\n{DUAL_EXTRACTION_PROMPT}"

    try:
        raw_output = call_vision_ai([b64], prompt)
        parsed = clean_json_response(raw_output)
        scenes = parsed.get("scenes", [])

        # Enrich each scene with page references
        for sc in scenes:
            sc["page_file"] = image_path.name
            sc["page_number"] = page_num
            sc["chapter"] = chapter_num
            # Ensure dialogue formatting follows convention: "(emotion) dialogue"
            emo = sc.get("voice_emotion", "").strip()
            dial = sc.get("dialogue_text", "").strip()
            if emo and not dial.startswith("("):
                sc["full_tts_script"] = f"{emo} {dial}".strip()
            else:
                sc["full_tts_script"] = dial

        return scenes
    except Exception as e:
        print(f"  [WARN] Failed to analyze page {image_path.name}: {e}")
        # Fallback scene stub
        return [{
            "scene_title": f"Page {page_num} Overview",
            "panel_location": "full-page",
            "speaker": "Narrator",
            "voice_emotion": "(neutral, observant)",
            "dialogue_text": f"Chapter {chapter_num} page {page_num} scene progression.",
            "full_tts_script": f"(neutral, observant) Chapter {chapter_num} page {page_num} scene progression.",
            "action_description": f"Visual panel sequence on page {page_num}.",
            "video_animation_prompt": f"Cinematic slow zoom into manga panel page {page_num}, detailed line art, atmospheric shadow and light.",
            "camera_movement": "Slow continuous push-in",
            "visual_style_fx": "Dark fantasy manga aesthetic with subtle lighting bloom",
            "estimated_duration_sec": 4.0,
            "page_file": image_path.name,
            "page_number": page_num,
            "chapter": chapter_num,
        }]


def export_scenes(
    chapter_dir: Path,
    all_scenes: list[dict],
    output_csv: Optional[Path],
    manga_title: str,
    chapter_num: str,
) -> tuple[list[dict], Path]:
    """Write prompt artifacts from already analyzed canonical scenes."""
    if output_csv is None:
        output_csv = chapter_dir / "video_prompts.csv"

    fieldnames = [
        "Scene_Number", "Chapter", "Page_File", "Character_Speaker",
        "Dialogue_Script", "Voice_Emotion_Cue", "Action_Description",
        "Video_Animation_Prompt", "Camera_Movement", "Visual_Style_FX",
        "Estimated_Duration_Sec",
    ]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for sc in all_scenes:
            writer.writerow({
                "Scene_Number": sc.get("scene_number"),
                "Chapter": sc.get("chapter"),
                "Page_File": sc.get("page_file"),
                "Character_Speaker": sc.get("speaker"),
                "Dialogue_Script": sc.get("full_tts_script") or sc.get("dialogue_text"),
                "Voice_Emotion_Cue": sc.get("voice_emotion"),
                "Action_Description": sc.get("action_description"),
                "Video_Animation_Prompt": sc.get("video_animation_prompt"),
                "Camera_Movement": sc.get("camera_movement"),
                "Visual_Style_FX": sc.get("visual_style_fx"),
                "Estimated_Duration_Sec": sc.get("estimated_duration_sec"),
            })

    json_path = chapter_dir / "pipeline_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "title": manga_title,
            "chapter": chapter_num,
            "total_scenes": len(all_scenes),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "scenes": all_scenes,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n[COMPLETE] Generated {len(all_scenes)} scenes:")
    print(f"  - CSV Prompts: {output_csv}")
    print(f"  - JSON Data:   {json_path}")
    return all_scenes, output_csv


def export_canonical_analysis(
    chapter_dir: Path,
    output_csv: Optional[Path] = None,
) -> tuple[list[dict], Path]:
    """Flatten complete sequential analysis without rereading source pages."""
    analysis_path = chapter_dir / "chapter_analysis.json"
    data = json.loads(analysis_path.read_text(encoding="utf-8"))
    if data.get("pages_analyzed") != data.get("total_pages"):
        raise ValueError(f"Canonical analysis incomplete: {analysis_path}")
    chapter_num = str(data.get("chapter") or chapter_dir.name.removeprefix("ch") or "1")
    scenes = []
    for page in data.get("pages", []):
        for scene in page.get("scenes", []):
            item = dict(scene)
            item["page_file"] = page.get("page_file", item.get("page_file"))
            item["page_number"] = page.get("page_number", item.get("page_number"))
            item["chapter"] = chapter_num
            item["scene_number"] = len(scenes) + 1
            emo = str(item.get("voice_emotion") or "").strip()
            dial = str(item.get("dialogue_text") or "").strip()
            item["full_tts_script"] = dial if not emo or dial.startswith("(") else f"{emo} {dial}".strip()
            scenes.append(item)
    if not scenes:
        raise ValueError(f"Canonical analysis has no scenes: {analysis_path}")
    title = str(data.get("title") or "Manga Series")
    return export_scenes(chapter_dir, scenes, output_csv, title, chapter_num)


def process_chapter(
    chapter_dir: Path,
    output_csv: Optional[Path] = None,
    max_pages: Optional[int] = None,
    start_page: int = 1,
) -> tuple[list[dict], Path]:
    """
    Runs Subagent 1 & Subagent 2 across chapter images, compiles results,
    and produces the comprehensive CSV file.
    """
    chapter_dir = chapter_dir.resolve()
    images_dir = chapter_dir / "images"
    if not images_dir.exists():
        raise FileNotFoundError(f"Images directory not found at {images_dir}")

    # Read metadata if present
    meta_path = chapter_dir / "metadata.json"
    manga_title = "Manga Series"
    chapter_num = chapter_dir.name.replace("ch", "") or "1"
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                manga_title = meta.get("title", manga_title)
                chapter_num = str(meta.get("chapter", {}).get("chapter", chapter_num))
        except Exception:
            pass

    # Collect images
    image_files = sorted(list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png")) + list(images_dir.glob("*.webp")))
    if not image_files:
        raise FileNotFoundError(f"No image files found in {images_dir}")

    # Slice page range
    end_idx = len(image_files) if not max_pages else min(start_page - 1 + max_pages, len(image_files))
    target_images = image_files[start_page - 1 : end_idx]

    print(f"\n{'='*60}")
    print(f"  RUNNING SUBAGENT 1 & 2 PROCESSING: {manga_title} (Ch {chapter_num})")
    print(f"  Pages to analyze: {len(target_images)} (from {start_page} to {end_idx})")
    print(f"{'='*60}")

    all_scenes = []
    global_scene_counter = 1

    for idx, img_path in enumerate(target_images, start=start_page):
        print(f"\n[ANALYSIS] Page {idx}/{len(image_files)}: {img_path.name}...")
        t0 = time.time()
        scenes = process_page(img_path, idx, chapter_num)
        dt = time.time() - t0

        for sc in scenes:
            sc["scene_number"] = global_scene_counter
            global_scene_counter += 1
            all_scenes.append(sc)

        print(f"  -> Extracted {len(scenes)} scene(s) in {dt:.1f}s")
        time.sleep(0.3)

    # Output CSV file
    if output_csv is None:
        output_csv = chapter_dir / "video_prompts.csv"

    fieldnames = [
        "Scene_Number",
        "Chapter",
        "Page_File",
        "Character_Speaker",
        "Dialogue_Script",
        "Voice_Emotion_Cue",
        "Action_Description",
        "Video_Animation_Prompt",
        "Camera_Movement",
        "Visual_Style_FX",
        "Estimated_Duration_Sec",
    ]

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for sc in all_scenes:
            writer.writerow({
                "Scene_Number": sc.get("scene_number"),
                "Chapter": sc.get("chapter"),
                "Page_File": sc.get("page_file"),
                "Character_Speaker": sc.get("speaker"),
                "Dialogue_Script": sc.get("full_tts_script") or sc.get("dialogue_text"),
                "Voice_Emotion_Cue": sc.get("voice_emotion"),
                "Action_Description": sc.get("action_description"),
                "Video_Animation_Prompt": sc.get("video_animation_prompt"),
                "Camera_Movement": sc.get("camera_movement"),
                "Visual_Style_FX": sc.get("visual_style_fx"),
                "Estimated_Duration_Sec": sc.get("estimated_duration_sec"),
            })

    # Also save complete JSON structured dataset
    json_path = chapter_dir / "pipeline_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "title": manga_title,
            "chapter": chapter_num,
            "total_scenes": len(all_scenes),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "scenes": all_scenes,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n[COMPLETE] Generated {len(all_scenes)} scenes:")
    print(f"  - CSV Prompts: {output_csv}")
    print(f"  - JSON Data:   {json_path}")
    return all_scenes, output_csv


def main():
    parser = argparse.ArgumentParser(description="Subagent 1 & 2 Script, Video Prompt & CSV Engine")
    parser.add_argument("--chapter-dir", "-d", required=True, help="Directory containing images/ and metadata.json")
    parser.add_argument("--output-csv", "-o", default=None, help="Output CSV filepath")
    parser.add_argument("--max-pages", "-m", type=int, default=None, help="Max pages to process")
    parser.add_argument("--start-page", "-s", type=int, default=1, help="Start page index (1-based)")
    args = parser.parse_args()

    ch_dir = Path(args.chapter_dir)
    out_csv = Path(args.output_csv) if args.output_csv else None
    canonical = ch_dir / "chapter_analysis.json"
    if canonical.exists() and args.max_pages is None and args.start_page == 1:
        print(f"[CANONICAL] Exporting prompts from {canonical}; no page reread")
        export_canonical_analysis(ch_dir, output_csv=out_csv)
    else:
        process_chapter(ch_dir, output_csv=out_csv, max_pages=args.max_pages, start_page=args.start_page)


if __name__ == "__main__":
    main()
