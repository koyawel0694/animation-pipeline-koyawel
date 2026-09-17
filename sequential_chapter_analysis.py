#!/usr/bin/env python3
"""Sequential canonical manga page analysis using agy medium effort."""
import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path

AGY = os.environ.get("AGY_BIN", "/home/john/.local/bin/agy")

PROMPT = """Read manga/manhwa page image at {image_path}.
You are the single canonical sequential reader for Chapter {chapter}.
Page number: {page_number}. Preserve continuity from prior pages when context is supplied.

Return ONLY valid JSON, no markdown fences, exactly this shape:
{{"page_number": {page_number}, "page_file": "{page_file}", "scenes": [{{"scene_title":"short title", "panel_location":"top/center/bottom/full-page", "speaker":"character name, role, or Narrator", "text_type":"spoken/narration/thought/sfx/caption/unknown", "voice_emotion":"(emotion, tone) or empty string", "dialogue_text":"exact readable dialogue or empty string", "action_description":"precise visible action, facial expression, blocking, setting", "story_flow":"how this page advances the story", "video_animation_prompt":"detailed image-to-video prompt preserving original line art and character identity", "camera_movement":"specific camera movement", "visual_style_fx":"lighting, atmosphere, and effects", "estimated_duration_sec":4.0}}]}}

Rules:
- Transcribe readable speech bubbles, narration boxes, thought bubbles, captions, and important SFX exactly.
- Never invent text. If visible text cannot be read, use "[unreadable]".
- Use one scene per meaningful panel or beat. Keep page order.
- Classify text as spoken, narration, thought, sfx, caption, or unknown. SFX is not spoken dialogue.
- Use an empty voice_emotion for SFX/captions when no delivery applies. Parenthesized emotion cue must describe delivery; dialogue_text itself stays verbatim.
- Describe only visible facts for action; mark uncertain identity as uncertain.
- Keep output valid JSON."""


def parse_json(text: str) -> dict:
    text = text.strip()
    if "```" in text:
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def validate_page(data: dict, page_num: int) -> dict:
    """Reject malformed model output before it becomes canonical source data."""
    if not isinstance(data, dict) or not isinstance(data.get("scenes"), list) or not data["scenes"]:
        raise ValueError("canonical page output must contain a non-empty scenes list")
    for scene in data["scenes"]:
        if not isinstance(scene, dict):
            raise ValueError("scene entry is not an object")
        for field in ("scene_title", "dialogue_text", "action_description", "story_flow", "camera_movement", "visual_style_fx"):
            if field not in scene or not isinstance(scene[field], str):
                raise ValueError(f"scene is missing string field {field}")
        if "text_type" in scene and scene["text_type"] not in {"spoken", "narration", "thought", "sfx", "caption", "unknown"}:
            raise ValueError(f"invalid text_type {scene['text_type']!r}")
    data["page_number"] = page_num
    return data


def save_json(path: Path, payload: dict) -> None:
    """Commit a complete JSON file atomically so interruption cannot corrupt it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp.replace(path)


def analyze_page(image_path: Path, page_num: int, chapter: str, prior_summary: str, effort: str = "medium") -> dict:
    prompt = PROMPT.format(
        image_path=str(image_path),
        page_number=page_num,
        page_file=image_path.name,
        chapter=chapter,
    )
    if prior_summary:
        prompt += "\nPrior continuity notes from already-read pages:\n" + prior_summary[-5000:]
    result = subprocess.run(
        [AGY, "--effort", effort, "-p", prompt],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"agy exited {result.returncode}")
    data = validate_page(parse_json(result.stdout), page_num)
    data["page_file"] = image_path.name
    if not isinstance(data.get("scenes"), list):
        raise ValueError("missing scenes list")
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter-dir", required=True)
    ap.add_argument("--output", default=None)
    ap.add_argument("--effort", default="medium", choices=["low", "medium", "high"], help="Reasoning effort for agy (low, medium, high)")
    args = ap.parse_args()
    effort = args.effort
    chapter_dir = Path(args.chapter_dir).resolve()
    output = Path(args.output) if args.output else chapter_dir / "chapter_analysis.json"
    metadata = {}
    metadata_path = chapter_dir / "metadata.json"
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid metadata JSON: {metadata_path}: {exc}")
    title = str(metadata.get("title") or chapter_dir.parent.name.replace("-", " ") or "Manga Series")
    chapter_meta = metadata.get("chapter")
    if isinstance(chapter_meta, dict):
        chapter = str(chapter_meta.get("chapter") or "")
    else:
        chapter = str(chapter_meta or "")
    if not chapter:
        match = re.search(r"(?:^|/)ch([^/]+)$", str(chapter_dir))
        chapter = match.group(1) if match else "1"
    images = sorted(
        list((chapter_dir / "images").glob("*.webp"))
        + list((chapter_dir / "images").glob("*.jpg"))
        + list((chapter_dir / "images").glob("*.jpeg"))
        + list((chapter_dir / "images").glob("*.png")),
        key=lambda path: (
            int(match.group(1)) if (match := re.search(r"page_(\d+)", path.stem)) else 10**9,
            path.name,
        )
    )
    if not images:
        raise SystemExit("No chapter images found")
    page_numbers = [
        int(match.group(1))
        for image in images
        if (match := re.search(r"page_(\d+)", image.stem))
    ]
    if page_numbers != list(range(1, len(images) + 1)):
        raise SystemExit(f"Chapter images must be page_001..page_NNN without gaps; found {page_numbers}")
    existing = {}
    if output.exists():
        try:
            old = json.loads(output.read_text())
            same_identity = (
                str(old.get("title") or "") == title
                and str(old.get("chapter") or "") == chapter
            )
            if same_identity:
                existing = {}
                for page in old.get("pages", []):
                    if "page_number" not in page or "page_file" not in page:
                        continue
                    try:
                        existing[int(page["page_number"])] = validate_page(page, int(page["page_number"]))
                    except (TypeError, ValueError):
                        continue
            print(f"Resuming existing canonical analysis: {len(existing)} pages")
        except Exception:
            pass
    pages = []
    for idx, image in enumerate(images, 1):
        if idx in existing and existing[idx].get("page_file") == image.name:
            pages.append(existing[idx])
            print(f"[SKIP] Page {idx}/{len(images)} already analyzed")
            continue
        print(f"[ANALYZE] Page {idx}/{len(images)}: {image.name}", flush=True)
        prior = "\n".join(
            f"Page {p['page_number']}: " + " ".join(s.get("story_flow", "") for s in p.get("scenes", []))
            for p in pages[-3:]
        )
        last_error = None
        for attempt in range(1, 4):
            try:
                page = analyze_page(image, idx, chapter, prior, effort=effort)
                pages.append(page)
                break
            except Exception as exc:
                last_error = str(exc)
                print(f"[RETRY] Page {idx}, attempt {attempt}: {last_error}", flush=True)
                time.sleep(2 * attempt)
        else:
            raise RuntimeError(f"Page {idx} failed after retries: {last_error}")
        payload = {
            "title": title,
            "chapter": chapter,
            "analysis_mode": "single sequential reader",
            "agy_effort": effort,
            "pages_analyzed": len(pages),
            "total_pages": len(images),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pages": pages,
        }
        save_json(output, payload)
        print(f"[SAVED] {len(pages)}/{len(images)} pages", flush=True)
    payload = {
        "title": title,
        "chapter": chapter,
        "analysis_mode": "single sequential reader",
        "agy_effort": effort,
        "pages_analyzed": len(pages),
        "total_pages": len(images),
        "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pages": pages,
    }
    save_json(output, payload)
    print(f"[COMPLETE] {output} ({len(pages)} pages)")


if __name__ == "__main__":
    main()
