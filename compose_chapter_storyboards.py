#!/usr/bin/env python3
"""Compose chapter storyboard sheets from approved clean visual frames.

Character refs are identity references only. Existing series refs can be supplied
with --reference-dir; no character sheets are regenerated or copied.
"""
import argparse
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 768, 1376
ROWS = [(2, 210), (1, 210), (2, 210), (2, 210), (1, 240)]
SLOTS = [0, 1, 2, 3, 3, 4, 4, 5]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "block"


def font(size: int, bold: bool = False):
    name = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(name, size) if Path(name).exists() else ImageFont.load_default()


def load_storyboard(chapter_dir: Path):
    path = chapter_dir / "storyboard_9_16.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    blocks = data.get("blocks", [])
    if not blocks:
        raise ValueError(f"No storyboard blocks in {path}")
    return data, blocks


def source_frames(chapter_dir: Path):
    source_dir = chapter_dir / "clean_frame_crops"
    frames = sorted(source_dir.glob("*.png"))
    if not frames:
        raise FileNotFoundError(f"No clean frame crops in {source_dir}")
    return frames


def choose_base(frames, block_index: int):
    # b01 is known anti-piracy artwork in this chapter; never use it.
    wanted = 2 if block_index == 1 else min(block_index, 6)
    matches = [p for p in frames if re.search(rf"b{wanted:02d}_", p.name)]
    if matches:
        return matches[0]
    safe = [p for p in frames if "b01_" not in p.name]
    return safe[(block_index - 1) % len(safe)]


def safe_frames(frames):
    """Reject known scanlation/promotional inserts from visual assets."""
    return [p for p in frames if "b01_" not in p.name]


def make_variation(source: Path, output: Path, variant: int):
    img = Image.open(source).convert("RGB")
    # Create distinct storyboard shots from one approved frame without stretching.
    zoom = [1.0, 1.08, 1.16, 1.24, 1.10, 1.20, 1.04, 1.14][variant]
    scale = max(768 / img.width, 1152 / img.height) * zoom
    resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
    max_left = max(0, resized.width - 768)
    max_top = max(0, resized.height - 1152)
    left = int(max_left * ((variant * 37) % 100) / 100)
    top = int(max_top * ((variant * 61) % 100) / 100)
    crop = resized.crop((left, top, left + 768, top + 1152))
    crop.save(output, optimize=True)


def compose_sheet(chapter_title: str, block: dict, frames: list[Path], output: Path):
    sheet = Image.new("RGB", (W, H), "#050505")
    draw = ImageDraw.Draw(sheet)
    header_h = 78
    draw.rectangle((0, 0, W, header_h), fill="#050505")
    title = f"SERYE DRAMA BLOCK — {chapter_title} — {block.get('block_title', 'Untitled')}"
    draw.text((W // 2, header_h // 2), title, fill="white", font=font(17, True), anchor="mm")

    beats = block.get("beats", [])
    y = header_h
    frame_index = 0
    for cols, height in ROWS:
        gap = 4
        cell_w = (W - gap * (cols - 1)) // cols
        for col in range(cols):
            idx = frame_index
            frame_index += 1
            img = Image.open(frames[idx]).convert("RGB")
            scale = max(cell_w / img.width, (height - 30) / img.height)
            img = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
            left = max(0, (img.width - cell_w) // 2)
            top = max(0, (img.height - (height - 30)) // 2)
            crop = img.crop((left, top, left + cell_w, top + height - 30))
            x = col * (cell_w + gap)
            sheet.paste(crop, (x, y))
            draw.rectangle((x, y + height - 30, x + cell_w, y + height), fill="#050505")
            beat = beats[SLOTS[idx]] if beats else {}
            label = str(beat.get("label", f"BEAT {SLOTS[idx] + 1}"))
            timestamp = str(beat.get("timestamp", ""))
            draw.text((x + cell_w // 2, y + height - 15), f"{timestamp}: {label}", fill="white", font=font(12, True), anchor="mm")
        y += height + 4
    sheet.save(output, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter-dir", required=True, type=Path)
    ap.add_argument("--reference-dir", required=True, type=Path)
    ap.add_argument("--output-dir", type=Path, default=None)
    args = ap.parse_args()

    chapter_dir = args.chapter_dir.resolve()
    ref_dir = args.reference_dir.resolve()
    if not ref_dir.is_dir() or not list(ref_dir.glob("*.png")):
        raise FileNotFoundError(f"Character reference directory has no PNGs: {ref_dir}")
    data, blocks = load_storyboard(chapter_dir)
    crops = safe_frames(source_frames(chapter_dir))
    if not crops:
        raise ValueError("No approved narrative frame crops remain after promotional-content filtering")
    output_dir = (args.output_dir or chapter_dir / "nano_storyboards").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "chapter_dir": str(chapter_dir),
        "character_reference_dir": str(ref_dir),
        "source_frames": [str(p) for p in crops],
        "blocks": [],
        "method": "local composition from approved clean frame crops",
    }
    title = data.get("title", "Manga Chapter")
    for block_index, block in enumerate(blocks, 1):
        base = choose_base(crops, block_index)
        frame_dir = chapter_dir / ".storyboard_work" / f"block{block_index:02d}"
        frame_dir.mkdir(parents=True, exist_ok=True)
        frames = []
        for slot in range(8):
            frame = frame_dir / f"frame_{slot + 1:02d}.png"
            make_variation(base, frame, slot)
            frames.append(frame)
        out = output_dir / f"block{block_index:02d}_{slugify(block.get('block_title', 'block'))}.png"
        compose_sheet(title, block, frames, out)
        manifest["blocks"].append({"block": block_index, "source_frame": str(base), "output": str(out)})
        print(f"[OK] {out}", flush=True)

    (chapter_dir / "storyboard_assets_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (chapter_dir / "character_refs_source.json").write_text(json.dumps({
        "source_dir": str(ref_dir),
        "files": [str(p) for p in sorted(ref_dir.glob("*.png"))],
        "reused": True,
    }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
