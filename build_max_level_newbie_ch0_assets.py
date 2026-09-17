#!/usr/bin/env python3
"""Build Chapter 0 SERYE metadata, clean crops, and 9:16 storyboard sheets.

This is intentionally chapter-specific: it uses the canonical sequential analysis
as the only narrative source and does not use the legacy Investor block template.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 768, 1376
TIMESTAMPS = ["0s-1.5s", "1.5s-3s", "3s-4.5s", "4.5s-6s", "6s-8s", "8s-10s"]
# Eight visual slots mapped to the six timing beats: 2+1+2+2+1.
SLOT_BEATS = [0, 1, 2, 3, 3, 4, 4, 5]
ROWS = [(2, 230), (1, 230), (2, 230), (2, 230), (1, 350)]


def clean_text(value: object) -> str:
    return " ".join(str(value or "").replace("\n", " ").split())


def english_text(value: object) -> str:
    """Keep prompt dialogue English-only while preserving readable ASCII text."""
    text = clean_text(value)
    # Canonical analysis may contain Korean SFX; those are visual/audio notes, not
    # spoken English lines for Flow/Kling. Drop non-ASCII runs from exported VO.
    text = re.sub(r"[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def emotion_tag(value: object) -> str:
    tag = clean_text(value)
    if not tag:
        return "(restrained, atmospheric)"
    if not tag.startswith("("):
        tag = f"({tag})"
    return tag


def safe_label(title: str) -> str:
    label = re.sub(r"[^A-Za-z0-9 ':/&-]", "", clean_text(title)).upper()
    return label[:34] or "UNTITLED BEAT"


def font(size: int, bold: bool = False):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size) if Path(path).exists() else ImageFont.load_default()


def select_scenes(scenes: list[dict], count: int = 6) -> list[tuple[int, dict]]:
    if not scenes:
        return [(0, {"scene_title": "Atmospheric transition", "action_description": "No scene description was available.", "camera_movement": "Locked camera", "voice_emotion": "(quiet, atmospheric)", "dialogue_text": "", "visual_style_fx": "Muted cinematic lighting", "story_flow": "Transition."}) for _ in range(count)]
    if len(scenes) == 1:
        return [(0, scenes[0]) for _ in range(count)]
    indices = []
    for i in range(count):
        index = round(i * (len(scenes) - 1) / (count - 1))
        if index in indices and index + 1 < len(scenes):
            index += 1
        indices.append(index)
    return [(index, scenes[index]) for index in indices]


def build_story(analysis: dict) -> dict:
    pages = analysis.get("pages") or []
    blocks = []
    for block_number, page in enumerate(pages, 1):
        scenes = page.get("scenes") or []
        chosen = select_scenes(scenes)
        title = clean_text((scenes[0] if scenes else {}).get("scene_title")) or f"Chapter 0 Page {block_number}"
        beats = []
        for beat_number, (scene_index, scene) in enumerate(chosen):
            dialogue = english_text(scene.get("dialogue_text"))
            # Credits/title-card OCR is not spoken dialogue; do not export it as VO.
            if "WAN.Z" in dialogue.upper() or not re.search(r"[A-Za-z]{2,}", dialogue):
                dialogue = ""
            vo = f"{emotion_tag(scene.get('voice_emotion'))} {dialogue}".strip() if dialogue else "none (no spoken English line; use environmental sound only)"
            action = english_text(scene.get("action_description"))
            camera = clean_text(scene.get("camera_movement")) or "Controlled cinematic camera movement"
            sfx = english_text(scene.get("visual_style_fx")) or "Atmospheric sound design"
            sfx = re.sub(r"\bwatermark\b", "clean title-card", sfx, flags=re.IGNORECASE)
            if beat_number == 5:
                action += " End on a complete freeze frame: hold the final pose with no new action."
                camera += "; then lock completely static through 10s"
                sfx += "; final impact resolves into silence"
            beats.append({
                "timestamp": TIMESTAMPS[beat_number],
                "label": safe_label(scene.get("scene_title") or f"BEAT {beat_number + 1}"),
                "page_number": page.get("page_number", block_number),
                "page_file": page.get("page_file", f"page_{block_number:03d}.jpg"),
                "scene_title": title if not scene.get("scene_title") else clean_text(scene.get("scene_title")),
                "action": action,
                "camera": camera,
                "vo": vo,
                "sfx": sfx,
                "story_flow": clean_text(scene.get("story_flow")),
                "source_scene_index": scene_index,
                "source_scene_count": len(scenes),
                "source_crop_ratio": (scene_index + 0.5) / max(1, len(scenes)),
            })
        blocks.append({
            "block_title": title,
            "duration_sec": 10,
            "format": "9:16 vertical",
            "beats": beats,
            "source_pages": [page.get("page_number", block_number)],
        })
    return {
        "title": analysis.get("title") or "I'm the Max-Level Newbie",
        "chapter": str(analysis.get("chapter") or "0"),
        "format": "SERYE drama block storyboard",
        "block_duration_sec": 10,
        "analysis_source": "chapter_analysis.json; single sequential reader",
        "blocks": blocks,
    }


def md_story(story: dict) -> str:
    lines = [
        f"SERYE Drama Storyboard — {story['title']} — Chapter {story['chapter']}",
        "",
        "Format: 9:16 vertical; six 10-second blocks; six timestamped beats per block; final beat freezes.",
        "",
    ]
    for number, block in enumerate(story["blocks"], 1):
        lines += [f"BLOCK {number} — {block['block_title']}", "", "| Time | Label | Source | Action | Camera | English VO | Sound / FX |", "|---|---|---|---|---|---|---|"]
        for beat in block["beats"]:
            vals = [beat.get(k, "") for k in ("timestamp", "label", "page_file", "action", "camera", "vo", "sfx")]
            vals = [str(v).replace("|", "\\|").replace("\n", " ") for v in vals]
            lines.append("| " + " | ".join(vals) + " |")
        lines += ["", "FINAL BEAT: complete freeze frame through 10s; no new action after the final pose.", "", "---", ""]
    return "\n".join(lines)


def html_story(story: dict) -> str:
    out = ["<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>SERYE Storyboard</title><style>",
            "body{margin:0;background:#090b10;color:#f3f5f8;font:14px/1.45 system-ui,sans-serif}main{max-width:1500px;margin:auto;padding:24px}h1{font-size:30px;margin:0 0 8px}.sub{color:#abb6c8;margin-bottom:22px}.block{background:#141a25;border:1px solid #354052;border-radius:12px;padding:16px;margin:0 0 24px}.block h2{margin:3px 0 15px;color:#67d9ff}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}.beat{background:#0d1119;border:1px solid #354052;border-radius:8px;padding:10px;min-width:0}.beat h3{font-size:13px;color:#f3c552;margin:0 0 6px}.beat p{font-size:12px;color:#b8c2d1;margin:5px 0}.beat b{color:#fff}.freeze{margin-top:12px;border:1px solid #f3c552;border-radius:6px;padding:8px;color:#f3c552;font-weight:700}@media(max-width:850px){.grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:560px){main{padding:12px}.grid{grid-template-columns:1fr}}</style></head><body><main>"]
    out.append(f"<h1>SERYE DRAMA STORYBOARD — {html.escape(str(story['title']))} — CHAPTER {html.escape(str(story['chapter']))}</h1>")
    out.append("<div class='sub'>Canonical sequential analysis · 9:16 · six blocks · six beats per block · English VO only</div>")
    for number, block in enumerate(story["blocks"], 1):
        out.append(f"<section class='block'><div>BLOCK {number}</div><h2>{html.escape(str(block['block_title']))}</h2><div class='grid'>")
        for beat in block["beats"]:
            out.append("<article class='beat'>")
            out.append(f"<h3>{html.escape(str(beat['timestamp']))} — {html.escape(str(beat['label']))}</h3>")
            out.append(f"<p><b>Source:</b> {html.escape(str(beat['page_file']))}</p><p><b>Action:</b> {html.escape(str(beat['action']))}</p><p><b>Camera:</b> {html.escape(str(beat['camera']))}</p><p><b>VO:</b> {html.escape(str(beat['vo']))}</p><p><b>FX:</b> {html.escape(str(beat['sfx']))}</p>")
            out.append("</article>")
        out.append("</div><div class='freeze'>FINAL BEAT: complete freeze frame through 10s; no new action after the final pose.</div></section>")
    out.append("</main></body></html>")
    return "".join(out)


def crop_frame(source: Path, output: Path, ratio: float, variant: int) -> None:
    with Image.open(source) as original:
        image = original.convert("RGB")
    width, height = image.size
    crop_height = min(height, max(2, int(width * 1.5)))
    # Variant offsets keep the duplicated two-panel beats visually distinct.
    center = max(0.0, min(1.0, ratio + (variant - 0.5) * 0.035))
    top = int(center * height - crop_height / 2)
    top = max(0, min(height - crop_height, top))
    crop = image.crop((0, top, width, top + crop_height))
    crop = crop.resize((768, 1152), Image.Resampling.LANCZOS)
    crop.save(output, format="PNG", optimize=True)


def compose_sheet(title: str, block: dict, frame_paths: list[Path], output: Path, number: int) -> None:
    sheet = Image.new("RGB", (W, H), "#050505")
    draw = ImageDraw.Draw(sheet)
    header_h = 84
    draw.text((W // 2, 22), f"SERYE DRAMA BLOCK — {title.upper()} —", fill="white", font=font(14, True), anchor="mm")
    draw.text((W // 2, 57), f"BLOCK {number} — {block['block_title']}", fill="#f3c552", font=font(15, True), anchor="mm")
    y = header_h
    frame_index = 0
    beat_index_for_slot = SLOT_BEATS
    for cols, row_height in ROWS:
        gap = 4
        cell_w = (W - gap * (cols - 1)) // cols
        content_h = row_height - 30
        for col in range(cols):
            frame = Image.open(frame_paths[frame_index]).convert("RGB")
            scale = max(cell_w / frame.width, content_h / frame.height)
            resized = frame.resize((int(frame.width * scale), int(frame.height * scale)), Image.Resampling.LANCZOS)
            left = max(0, (resized.width - cell_w) // 2)
            top = max(0, (resized.height - content_h) // 2)
            crop = resized.crop((left, top, left + cell_w, top + content_h))
            x = col * (cell_w + gap)
            sheet.paste(crop, (x, y))
            draw.rectangle((x, y + content_h, x + cell_w, y + row_height), fill="#050505")
            beat = block["beats"][beat_index_for_slot[frame_index]]
            label = f"{beat['timestamp']} — {beat['label']}"
            draw.text((x + cell_w // 2, y + content_h + 15), label[:55], fill="white", font=font(9, True), anchor="mm")
            frame_index += 1
        y += row_height + 4
    sheet.save(output, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter-dir", required=True, type=Path)
    args = parser.parse_args()
    chapter = args.chapter_dir.resolve()
    analysis_path = chapter / "chapter_analysis.json"
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    story = build_story(analysis)
    (chapter / "storyboard_9_16.json").write_text(json.dumps(story, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (chapter / "storyboard_9_16.md").write_text(md_story(story), encoding="utf-8")
    (chapter / "storyboard_9_16.html").write_text(html_story(story), encoding="utf-8")

    crops_dir = chapter / "clean_frame_crops"
    crops_dir.mkdir(parents=True, exist_ok=True)
    storyboard_dir = chapter / "nano_storyboards"
    storyboard_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"chapter_dir": str(chapter), "dimensions": [768, 1376], "method": "deterministic crops from narrative source pages", "blocks": []}
    for number, block in enumerate(story["blocks"], 1):
        page = block["beats"][0]["page_file"]
        source = chapter / "images" / page
        frames = []
        for slot, beat_index in enumerate(SLOT_BEATS, 1):
            beat = block["beats"][beat_index]
            slug = re.sub(r"[^a-z0-9]+", "_", beat["label"].lower()).strip("_") or "beat"
            frame = crops_dir / f"b{number:02d}_s{slot:02d}_{slug}.png"
            crop_frame(source, frame, float(beat.get("source_crop_ratio", 0.5)), slot)
            frames.append(frame)
        block_slug = re.sub(r"[^a-z0-9]+", "_", block["block_title"].lower()).strip("_") or f"block_{number}"
        sheet = storyboard_dir / f"block{number:02d}_{block_slug}.png"
        compose_sheet(story["title"], block, frames, sheet, number)
        manifest["blocks"].append({"block": number, "output": str(sheet), "source_page": page, "frames": [str(p) for p in frames]})
    (chapter / "storyboard_assets_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[OK] Built {len(story['blocks'])} storyboard blocks, {sum(len(b['beats']) for b in story['blocks'])} beats and {len(manifest['blocks']) * 8} visual crops")


if __name__ == "__main__":
    main()
