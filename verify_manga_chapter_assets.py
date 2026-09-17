#!/usr/bin/env python3
"""Verify the complete, source-traceable manga chapter asset contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image

from chapter_contract import build_script_entries, flatten_scenes, script_cue, source_text


TIMESTAMPS = ["0s-1.5s", "1.5s-3s", "3s-4.5s", "4.5s-6s", "6s-8s", "8s-10s"]
IMAGE_SUFFIXES = {".webp", ".jpg", ".jpeg", ".png"}
TEXT_TYPES = {"spoken", "narration", "thought", "sfx", "caption", "unknown", "none"}


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
    files = sorted(
        (path for path in images_dir.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES),
        key=lambda path: (
            int(match.group(1)) if (match := re.search(r"page_(\d+)", path.stem)) else 10**9,
            path.name,
        ),
    ) if images_dir.is_dir() else []
    if not files:
        fail(errors, f"no chapter images in {images_dir}")
        return 0

    actual = []
    for path in files:
        match = re.search(r"page_(\d+)", path.stem)
        if not match:
            fail(errors, f"page file has no numeric order: {path.name}")
        else:
            actual.append(int(match.group(1)))
        try:
            with Image.open(path) as image:
                image.verify()
        except Exception as exc:
            fail(errors, f"unreadable page image {path}: {exc}")
    expected = list(range(1, len(files) + 1))
    if actual != expected:
        fail(errors, f"page numbering is not contiguous: {actual}")
    return len(files)


def check_metadata(chapter_dir: Path, page_count: int, errors: list[str]) -> dict | None:
    metadata = load_json(chapter_dir / "metadata.json", errors)
    if not metadata:
        return metadata
    if not str(metadata.get("title") or metadata.get("series_title") or "").strip():
        fail(errors, "metadata.json has no title")
    if not metadata.get("source_url") and not metadata.get("manga_url"):
        fail(errors, "metadata.json has no source_url or manga_url provenance")
    recorded_count = metadata.get("pages_count", metadata.get("page_count"))
    if recorded_count not in (None, page_count):
        fail(errors, f"metadata page count={recorded_count} but found {page_count} images")
    chapter = metadata.get("chapter")
    if not chapter or (isinstance(chapter, dict) and not chapter.get("chapter")):
        fail(errors, "metadata.json has no chapter identity")
    return metadata


def check_analysis(
    chapter_dir: Path,
    page_count: int,
    errors: list[str],
) -> tuple[dict | None, list[dict], list[dict]]:
    data = load_json(chapter_dir / "chapter_analysis.json", errors)
    if not data:
        return None, [], []
    if data.get("pages_analyzed") != page_count or data.get("total_pages") != page_count:
        fail(errors, "chapter_analysis.json does not cover every source page")
    pages = data.get("pages") or []
    numbers = [page.get("page_number") for page in pages]
    if numbers != list(range(1, page_count + 1)):
        fail(errors, f"analysis page numbers are not contiguous: {numbers}")
    source_names = {
        path.name
        for path in (chapter_dir / "images").iterdir()
        if path.is_file()
    } if (chapter_dir / "images").is_dir() else set()
    for page in pages:
        page_file = page.get("page_file")
        if page_file not in source_names:
            fail(errors, f"analysis references missing source page: {page_file}")
        scenes = page.get("scenes")
        if not isinstance(scenes, list) or not scenes:
            fail(errors, f"analysis page {page.get('page_number')} has no scenes")
            continue
        for scene_index, scene in enumerate(scenes, 1):
            if not isinstance(scene, dict):
                fail(errors, f"analysis page {page.get('page_number')} scene {scene_index} is not an object")
                continue
            for field in ("scene_title", "dialogue_text", "action_description", "story_flow", "camera_movement", "visual_style_fx"):
                if not isinstance(scene.get(field), str):
                    fail(errors, f"analysis page {page.get('page_number')} scene {scene_index} missing string field {field}")
            if scene.get("text_type") not in (None, "spoken", "narration", "thought", "sfx", "caption", "unknown"):
                fail(errors, f"analysis page {page.get('page_number')} scene {scene_index} has invalid text_type")
    scenes = flatten_scenes(data)
    return data, scenes, build_script_entries(scenes)


def check_script(
    chapter_dir: Path,
    analysis: dict | None,
    expected_entries: list[dict],
    errors: list[str],
) -> dict[str, dict]:
    script_path = chapter_dir / "chapter_script.json"
    script = load_json(script_path, errors)
    if not script:
        return {}
    for name in ("chapter_script.txt", "chapter_script.md"):
        if not (chapter_dir / name).exists():
            fail(errors, f"missing {chapter_dir / name}")
    actual_entries = script.get("lines") or []
    if script.get("line_count") != len(actual_entries):
        fail(errors, "chapter_script.json line_count does not match lines")
    if len(actual_entries) != len(expected_entries):
        fail(errors, f"chapter_script.json has {len(actual_entries)} lines; analysis has {len(expected_entries)}")
    fields = ("line_id", "page_number", "page_file", "text_type", "speaker", "voice_emotion", "dialogue_text")
    for index, (expected, actual) in enumerate(zip(expected_entries, actual_entries), 1):
        for field in fields:
            if actual.get(field) != expected.get(field):
                fail(errors, f"chapter_script line {index} field {field} does not match canonical analysis")
    if analysis:
        source_hash = script.get("source_analysis_sha256")
        analysis_path = chapter_dir / "chapter_analysis.json"
        if source_hash != hashlib.sha256(analysis_path.read_bytes()).hexdigest():
            fail(errors, "chapter_script.json source_analysis_sha256 does not match chapter_analysis.json")
    return {entry.get("line_id"): entry for entry in actual_entries if entry.get("line_id")}


def check_refs(chapter_dir: Path, errors: list[str]) -> None:
    source_manifest = load_json(chapter_dir / "character_refs_source.json", errors)
    ref_dir = chapter_dir / "character_refs"
    refs = sorted(ref_dir.glob("*.png")) if ref_dir.is_dir() else []
    if not refs and source_manifest:
        source_dir = Path(source_manifest.get("source_dir", ""))
        manifest_files = [Path(item) for item in (source_manifest.get("files") or []) if item]
        refs = [path for path in manifest_files if path.exists()]
        if not refs and source_dir.is_dir():
            refs = sorted(source_dir.glob("*.png"))
    if not refs:
        fail(errors, f"no character reference PNGs in {ref_dir} or its provenance source")
        return
    for path in refs:
        try:
            with Image.open(path) as image:
                if image.size != (768, 1376):
                    fail(errors, f"character reference must be 768x1376: {path.name} {image.size}")
                image.verify()
        except Exception as exc:
            fail(errors, f"invalid character reference {path}: {exc}")
    if source_manifest is not None:
        if not source_manifest.get("files"):
            fail(errors, "character_refs_source.json has no files")
        if not source_manifest.get("source_dir"):
            fail(errors, "character_refs_source.json has no source_dir")
        for listed in source_manifest.get("files") or []:
            if not Path(listed).exists():
                fail(errors, f"character_refs_source.json points to missing reference: {listed}")


def check_style(chapter_dir: Path, errors: list[str]) -> None:
    selection = load_json(chapter_dir / "style_selection.json", errors)
    if not selection:
        return
    config_path = Path(__file__).with_name("style_presets.json")
    try:
        presets = json.loads(config_path.read_text(encoding="utf-8")).get("presets") or {}
    except Exception as exc:
        fail(errors, f"invalid style preset configuration: {exc}")
        return
    if selection.get("default_preset") not in presets:
        fail(errors, f"unknown style preset in chapter selection: {selection.get('default_preset')!r}")


def check_storyboards(
    chapter_dir: Path,
    page_count: int,
    story: dict | None,
    script_by_id: dict[str, dict],
    scenes: list[dict],
    errors: list[str],
) -> tuple[int, int]:
    if not story:
        return 0, 0
    blocks = story.get("blocks") or []
    if not blocks:
        fail(errors, "storyboard_9_16.json has no blocks")
        return 0, 0
    if story.get("total_pages") != page_count:
        fail(errors, "storyboard total_pages does not match source images")
    if story.get("total_blocks") != len(blocks):
        fail(errors, "storyboard total_blocks does not match blocks")
    if story.get("total_duration_sec") != len(blocks) * 10:
        fail(errors, "storyboard duration is not 10 seconds per block")

    canonical_ids = {scene.get("_scene_key") for scene in scenes}
    seen_nontransitional: set[str] = set()
    for index, block in enumerate(blocks, 1):
        beats = block.get("beats") or []
        if len(beats) != 6:
            fail(errors, f"storyboard block {index} has {len(beats)} beats, expected 6")
            continue
        if block.get("block_number") != index:
            fail(errors, f"storyboard block {index} has unexpected block_number")
        actual = [str(beat.get("timestamp")) for beat in beats]
        if actual != TIMESTAMPS:
            fail(errors, f"storyboard block {index} timestamps are {actual}")
        final_text = " ".join(str(value or "") for value in beats[-1].values()).lower()
        if "freeze" not in final_text:
            fail(errors, f"storyboard block {index} has no final freeze-frame instruction")
        expected_line_ids = []
        for beat_index, beat in enumerate(beats, 1):
            source_id = beat.get("source_scene_id")
            if source_id not in canonical_ids:
                fail(errors, f"storyboard block {index} beat {beat_index} has unknown source_scene_id {source_id!r}")
            if not beat.get("action") or not beat.get("camera"):
                fail(errors, f"storyboard block {index} beat {beat_index} lacks action or camera")
            if beat.get("text_type") not in TEXT_TYPES:
                fail(errors, f"storyboard block {index} beat {beat_index} has invalid text_type")
            if beat.get("is_transitional"):
                if beat.get("script_line_id") or source_text(beat.get("source_text")):
                    fail(errors, f"transitional beat {index}.{beat_index} contains a script line")
            else:
                if source_id in seen_nontransitional:
                    fail(errors, f"canonical source scene {source_id} is replayed as a narrative beat")
                if source_id:
                    seen_nontransitional.add(source_id)
                line_id = beat.get("script_line_id")
                if line_id:
                    expected_line_ids.append(line_id)
                    line = script_by_id.get(line_id)
                    if not line:
                        fail(errors, f"storyboard block {index} references missing script line {line_id}")
                    elif line.get("dialogue_text") != beat.get("source_text"):
                        fail(errors, f"storyboard block {index} script line {line_id} text drifted from chapter script")
        if block.get("script_line_ids") != expected_line_ids:
            fail(errors, f"storyboard block {index} script_line_ids do not match its beats")

    expected_ranges = []
    episodes = story.get("episodes") or []
    for ep_index, episode in enumerate(episodes, 1):
        page_range = episode.get("page_range") or []
        if len(page_range) != 2:
            fail(errors, f"episode {ep_index} has no two-number page_range")
            continue
        expected_ranges.append(tuple(page_range))
        if episode.get("blocks_count") != 6:
            fail(errors, f"episode {ep_index} has {episode.get('blocks_count')} blocks, expected 6")
    if expected_ranges:
        if expected_ranges[0][0] != 1 or expected_ranges[-1][1] != page_count:
            fail(errors, "episode page ranges do not cover the complete chapter")
        for previous, current in zip(expected_ranges, expected_ranges[1:]):
            if current[0] != previous[1] + 1:
                fail(errors, f"episode page ranges overlap or contain a gap: {expected_ranges}")

    for name in ("storyboard_9_16.md", "storyboard_9_16.html", "episodes_manifest.json"):
        if not (chapter_dir / name).exists():
            fail(errors, f"missing storyboard artifact {chapter_dir / name}")
    if story.get("script_line_count") != len(script_by_id):
        fail(errors, "storyboard script_line_count does not match chapter_script.json")

    # Validate the standalone episode storyboards as well as the root master.
    if story.get("total_episodes", 1) > 1:
        episodes_dir = chapter_dir / "episodes"
        for ep_number in range(1, story["total_episodes"] + 1):
            ep_dir = episodes_dir / f"ep{ep_number:02d}"
            ep_story = load_json(ep_dir / "storyboard_9_16.json", errors)
            if not ep_story:
                continue
            ep_blocks = ep_story.get("blocks") or []
            if len(ep_blocks) != 6:
                fail(errors, f"episode {ep_number} storyboard has {len(ep_blocks)} blocks, expected 6")
            for local_index, block in enumerate(ep_blocks, 1):
                if block.get("episode_block_number") != local_index:
                    fail(errors, f"episode {ep_number} block {local_index} is not locally numbered")
            for name in ("storyboard_9_16.md", "storyboard_9_16.html", "chapter_script.json", "chapter_script.txt", "chapter_script.md"):
                if not (ep_dir / name).exists():
                    fail(errors, f"missing episode {ep_number} artifact {ep_dir / name}")

    return len(blocks), sum(len(block.get("beats") or []) for block in blocks)


def check_prompt_files(
    prompt_dir: Path,
    blocks: list[dict],
    errors: list[str],
    label: str,
) -> None:
    manifest = load_json(prompt_dir / "prompt_txt_manifest.json", errors)
    if manifest and len(manifest.get("blocks") or []) != len(blocks):
        fail(errors, f"{label} prompt_txt_manifest block count does not match storyboard")
    if manifest and not manifest.get("script_artifact"):
        fail(errors, f"{label} prompt manifest has no script_artifact")
    for local_index, block in enumerate(blocks, 1):
        shot_path = prompt_dir / f"block{local_index}_prompts.txt"
        video_path = prompt_dir / f"block{local_index}_video_prompt.txt"
        if not shot_path.exists():
            fail(errors, f"missing {shot_path}")
            continue
        parts = [part for part in shot_path.read_text(encoding="utf-8").split("@@@NEXT@@@") if part.strip()]
        if len(parts) != 6:
            fail(errors, f"{shot_path.name} contains {len(parts)} prompts, expected 6")
        for beat_index, (beat, part) in enumerate(zip(block.get("beats") or [], parts), 1):
            cue = script_cue(beat)
            if cue not in part:
                fail(errors, f"{shot_path.name} beat {beat_index} does not contain its exact manga script cue")
            if beat.get("source_scene_id") and beat.get("source_scene_id") not in part:
                fail(errors, f"{shot_path.name} beat {beat_index} lacks source scene identity")
        if parts and "freeze frame" not in parts[-1].lower():
            fail(errors, f"{shot_path.name} final prompt lacks freeze-frame instruction")
        if not video_path.exists():
            fail(errors, f"missing {video_path}")
        else:
            continuous = video_path.read_text(encoding="utf-8")
            cursor = 0
            for beat_index, beat in enumerate(block.get("beats") or [], 1):
                cue = script_cue(beat)
                position = continuous.find(cue, cursor)
                if position < 0:
                    fail(errors, f"{video_path.name} beat {beat_index} does not contain its exact manga script cue")
                else:
                    cursor = position + len(cue)
    expected_shots = len(blocks) * 6
    combined = prompt_dir / f"flow_all_{expected_shots}_shots.txt"
    if not combined.exists():
        fail(errors, f"missing combined shot TXT for {expected_shots} shots in {prompt_dir}")
    continuous = prompt_dir / f"flow_{len(blocks)}_continuous_blocks.txt"
    if not continuous.exists():
        fail(errors, f"missing {continuous}")


def check_prompts(
    chapter_dir: Path,
    story: dict | None,
    script_by_id: dict[str, dict],
    errors: list[str],
) -> None:
    if not story:
        return
    root_blocks = story.get("blocks") or []
    check_prompt_files(chapter_dir / "flow_queue", root_blocks, errors, "root")
    if story.get("total_episodes", 1) <= 1:
        return
    episodes_dir = chapter_dir / "episodes"
    for ep_number in range(1, story["total_episodes"] + 1):
        ep_dir = episodes_dir / f"ep{ep_number:02d}"
        ep_story = load_json(ep_dir / "storyboard_9_16.json", errors)
        if not ep_story:
            continue
        ep_script = load_json(ep_dir / "chapter_script.json", errors)
        if not ep_script:
            continue
        expected_ids = ep_story.get("script_line_ids") or []
        actual_lines = ep_script.get("lines") or []
        actual_ids = [line.get("line_id") for line in actual_lines]
        if actual_ids != expected_ids:
            fail(errors, f"episode {ep_number} chapter_script.json IDs do not match its storyboard")
        if ep_script.get("source_analysis_sha256") != hashlib.sha256(
            (chapter_dir / "chapter_analysis.json").read_bytes()
        ).hexdigest():
            fail(errors, f"episode {ep_number} script source hash does not match chapter_analysis.json")
        for line in actual_lines:
            canonical = script_by_id.get(line.get("line_id"))
            if not canonical:
                fail(errors, f"episode {ep_number} script references unknown line {line.get('line_id')}")
                continue
            for field in ("page_number", "page_file", "text_type", "speaker", "voice_emotion", "dialogue_text"):
                if line.get(field) != canonical.get(field):
                    fail(errors, f"episode {ep_number} script line {line.get('line_id')} field {field} drifted")
        if not actual_lines and expected_ids:
            fail(errors, f"episode {ep_number} script ledger is empty")
        check_prompt_files(
            ep_dir / "flow_queue",
            ep_story.get("blocks") or [],
            errors,
            f"episode {ep_number}",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify manga chapter production assets")
    parser.add_argument("--chapter-dir", required=True, type=Path)
    args = parser.parse_args()
    chapter_dir = args.chapter_dir.resolve()
    errors: list[str] = []
    page_count = check_images(chapter_dir, errors)
    check_metadata(chapter_dir, page_count, errors)
    analysis, scenes, expected_script = check_analysis(chapter_dir, page_count, errors)
    check_style(chapter_dir, errors)
    check_refs(chapter_dir, errors)
    script_by_id = check_script(chapter_dir, analysis, expected_script, errors)
    story = load_json(chapter_dir / "storyboard_9_16.json", errors)
    block_count, shot_count = check_storyboards(
        chapter_dir, page_count, story, script_by_id, scenes, errors
    )
    check_prompts(chapter_dir, story, script_by_id, errors)
    if errors:
        print("[FAIL]")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"[OK] {chapter_dir}: {page_count} pages, {block_count} blocks, {shot_count} beats verified "
        f"with {len(script_by_id)} source script lines"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
