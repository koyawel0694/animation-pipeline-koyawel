#!/usr/bin/env python3
"""Verify the focused manga chapter asset contract."""

import argparse
import json
import re
from pathlib import Path

from PIL import Image


TIMESTAMPS = ["0s-1.5s", "1.5s-3s", "3s-4.5s", "4.5s-6s", "6s-8s", "8s-10s"]
IMAGE_SUFFIXES = {".webp", ".jpg", ".jpeg", ".png"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]):
    if not path.exists():
        fail(errors, f"missing {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(errors, f"invalid JSON {path}: {exc}")
        return None


def check_images(chapter_dir: Path, errors: list[str]) -> int:
    images_dir = chapter_dir / "images"
    files = sorted(p for p in images_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES) if images_dir.is_dir() else []
    if not files:
        fail(errors, f"no chapter images in {images_dir}")
        return 0
    expected = list(range(1, len(files) + 1))
    actual = []
    for path in files:
        match = re.search(r"page_(\d+)", path.stem)
        if not match:
            fail(errors, f"page file has no numeric order: {path.name}")
            continue
        actual.append(int(match.group(1)))
        try:
            with Image.open(path) as image:
                image.verify()
        except Exception as exc:
            fail(errors, f"unreadable page image {path}: {exc}")
    if sorted(actual) != expected:
        fail(errors, f"page numbering is not contiguous: {actual}")
    return len(files)


def check_analysis(chapter_dir: Path, page_count: int, errors: list[str]) -> None:
    data = load_json(chapter_dir / "chapter_analysis.json", errors)
    if not data:
        return
    if data.get("pages_analyzed") != page_count or data.get("total_pages") != page_count:
        fail(errors, "chapter_analysis.json does not cover every source page")
    pages = data.get("pages") or []
    numbers = [p.get("page_number") for p in pages]
    if numbers != list(range(1, page_count + 1)):
        fail(errors, f"analysis page numbers are not contiguous: {numbers}")
    source_names = {p.name for p in (chapter_dir / "images").iterdir() if p.is_file()} if (chapter_dir / "images").is_dir() else set()
    missing = [p.get("page_file") for p in pages if p.get("page_file") not in source_names]
    if missing:
        fail(errors, f"analysis references missing source pages: {missing}")


def check_refs(chapter_dir: Path, errors: list[str]) -> None:
    ref_dir = chapter_dir / "character_refs"
    refs = sorted(ref_dir.glob("*.png")) if ref_dir.is_dir() else []
    if not refs:
        fail(errors, f"no character reference PNGs in {ref_dir}")
        return
    for path in refs:
        try:
            with Image.open(path) as image:
                if image.size[0] * 1376 != image.size[1] * 768:
                    fail(errors, f"character reference is not 9:16: {path.name} {image.size}")
                image.verify()
        except Exception as exc:
            fail(errors, f"invalid character reference {path}: {exc}")
    if not (chapter_dir / "character_refs_source.json").exists():
        fail(errors, "missing character_refs_source.json")


def check_storyboards(chapter_dir: Path, errors: list[str]) -> tuple[int, int]:
    data = load_json(chapter_dir / "storyboard_9_16.json", errors)
    if not data:
        return 0, 0
    blocks = data.get("blocks") or []
    if not blocks:
        fail(errors, "storyboard_9_16.json has no blocks")
        return 0, 0
    for index, block in enumerate(blocks, 1):
        beats = block.get("beats") or []
        if len(beats) != 6:
            fail(errors, f"storyboard block {index} has {len(beats)} beats, expected 6")
            continue
        actual = [str(beat.get("timestamp")) for beat in beats]
        if actual != TIMESTAMPS:
            fail(errors, f"storyboard block {index} timestamps are {actual}")
        final_text = " ".join(str(value or "") for value in beats[-1].values()).lower()
        if "freeze" not in final_text:
            fail(errors, f"storyboard block {index} has no final freeze-frame instruction")
    manifest_path = chapter_dir / "storyboard_assets_manifest.json"
    if manifest_path.exists():
        manifest = load_json(manifest_path, errors)
        manifest_blocks = (manifest or {}).get("blocks") or []
        if len(manifest_blocks) != len(blocks):
            fail(errors, f"storyboard manifest count {len(manifest_blocks)} does not match block count {len(blocks)}")
        sheets = []
        for item in manifest_blocks:
            output = item.get("output")
            if not output:
                fail(errors, "storyboard manifest has a block without an output path")
                continue
            path = Path(output)
            if not path.is_absolute():
                path = chapter_dir / path
            if not path.exists():
                fail(errors, f"storyboard manifest points to missing PNG: {path}")
            else:
                sheets.append(path)
        for path in sheets:
            try:
                with Image.open(path) as image:
                    if image.size[0] * 1376 != image.size[1] * 768:
                        fail(errors, f"storyboard is not 9:16: {path.name} {image.size}")
                    image.verify()
            except Exception as exc:
                fail(errors, f"invalid storyboard image {path}: {exc}")
    for name in ("storyboard_9_16.md", "storyboard_9_16.html"):
        if not (chapter_dir / name).exists():
            fail(errors, f"missing storyboard artifact {chapter_dir / name}")
    return len(blocks), sum(len(block.get("beats") or []) for block in blocks)


def check_prompt_txt(chapter_dir: Path, block_count: int, shot_count: int, errors: list[str]) -> None:
    prompt_dir = chapter_dir / "flow_queue"
    manifest = load_json(prompt_dir / "prompt_txt_manifest.json", errors)
    if manifest and len(manifest.get("blocks") or []) != block_count:
        fail(errors, "prompt_txt_manifest block count does not match storyboard")
    for index in range(1, block_count + 1):
        path = prompt_dir / f"block{index}_prompts.txt"
        if not path.exists():
            fail(errors, f"missing block prompt file {path}")
            continue
        parts = [part for part in path.read_text(encoding="utf-8").split("@@@NEXT@@@") if part.strip()]
        if len(parts) != 6:
            fail(errors, f"{path.name} contains {len(parts)} prompts, expected 6")
        if "freeze frame" not in parts[-1].lower():
            fail(errors, f"{path.name} final prompt lacks freeze-frame instruction")
    combined = sorted(prompt_dir.glob("flow_all_*_shots.txt")) if prompt_dir.is_dir() else []
    if not any(re.search(rf"flow_all_{shot_count}_shots\.txt$", str(path)) for path in combined):
        fail(errors, f"missing combined shot TXT for {shot_count} shots")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify manga chapter assets")
    parser.add_argument("--chapter-dir", required=True, type=Path)
    args = parser.parse_args()
    chapter_dir = args.chapter_dir.resolve()
    errors: list[str] = []
    metadata = load_json(chapter_dir / "metadata.json", errors)
    page_count = check_images(chapter_dir, errors)
    if metadata and metadata.get("pages_count") not in (None, page_count):
        fail(errors, f"metadata pages_count={metadata.get('pages_count')} but found {page_count} images")
    check_analysis(chapter_dir, page_count, errors)
    check_refs(chapter_dir, errors)
    block_count, shot_count = check_storyboards(chapter_dir, errors)
    check_prompt_txt(chapter_dir, block_count, shot_count, errors)
    if errors:
        print("[FAIL]")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"[OK] {chapter_dir}: {page_count} pages, {block_count} blocks, {shot_count} beats verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
