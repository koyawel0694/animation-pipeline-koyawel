#!/usr/bin/env python3
"""Sequential canonical manga page analysis using agy medium effort."""
import argparse
import json
import re
import subprocess
import time
from pathlib import Path

AGY = "/home/john/.local/bin/agy"

PROMPT = """Read manga/manhwa page image at {image_path}.
You are the single canonical sequential reader for Chapter {chapter}.
Page number: {page_number}. Preserve continuity from prior pages when context is supplied.

Return ONLY valid JSON, no markdown fences, exactly this shape:
{{"page_number": {page_number}, "page_file": "{page_file}", "scenes": [{{"scene_title":"short title", "panel_location":"top/center/bottom/full-page", "speaker":"character name, role, or Narrator", "voice_emotion":"(emotion, tone)", "dialogue_text":"exact readable dialogue or empty string", "action_description":"precise visible action, facial expression, blocking, setting", "story_flow":"how this page advances the story", "video_animation_prompt":"detailed image-to-video prompt preserving original line art and character identity", "camera_movement":"specific camera movement", "visual_style_fx":"lighting, atmosphere, and effects", "estimated_duration_sec":4.0}}]}}

Rules:
- Transcribe readable speech bubbles, narration boxes, thought bubbles, and important SFX exactly.
- Never invent text. If visible text cannot be read, use "[unreadable]".
- Use one scene per meaningful panel or beat. Keep page order.
- Parenthesized emotion cue must describe delivery; dialogue_text itself stays verbatim.
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


def analyze_page(image_path: Path, page_num: int, chapter: str, prior_summary: str) -> dict:
    prompt = PROMPT.format(
        image_path=str(image_path),
        page_number=page_num,
        page_file=image_path.name,
        chapter=chapter,
    )
    if prior_summary:
        prompt += "\nPrior continuity notes from already-read pages:\n" + prior_summary[-5000:]
    result = subprocess.run(
        [AGY, "--effort", "medium", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"agy exited {result.returncode}")
    data = parse_json(result.stdout)
    if data.get("page_number") != page_num:
        data["page_number"] = page_num
    data["page_file"] = image_path.name
    if not isinstance(data.get("scenes"), list):
        raise ValueError("missing scenes list")
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter-dir", required=True)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()
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
        + list((chapter_dir / "images").glob("*.png"))
    )
    if not images:
        raise SystemExit("No chapter images found")
    existing = {}
    if output.exists():
        try:
            old = json.loads(output.read_text())
            same_identity = (
                str(old.get("title") or "") == title
                and str(old.get("chapter") or "") == chapter
            )
            if same_identity:
                existing = {
                    p["page_number"]: p
                    for p in old.get("pages", [])
                    if "page_number" in p and "page_file" in p
                }
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
                page = analyze_page(image, idx, chapter, prior)
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
            "agy_effort": "medium",
            "pages_analyzed": len(pages),
            "total_pages": len(images),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pages": pages,
        }
        output.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[SAVED] {len(pages)}/{len(images)} pages", flush=True)
    payload = {
        "title": title,
        "chapter": chapter,
        "analysis_mode": "single sequential reader",
        "agy_effort": "medium",
        "pages_analyzed": len(pages),
        "total_pages": len(images),
        "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pages": pages,
    }
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[COMPLETE] {output} ({len(pages)} pages)")


if __name__ == "__main__":
    main()
