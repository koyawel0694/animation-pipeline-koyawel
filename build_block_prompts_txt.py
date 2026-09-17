#!/usr/bin/env python3
"""Export storyboard block prompts as plain-text Flow prompt files.

The storyboard JSON is the source of truth.  This exporter deliberately writes
plain text only; CSV is an optional legacy integration and is not required for
the manga chapter asset workflow.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


DELIMITER = "\n\n@@@NEXT@@@\n\n"
STYLE_CONFIG_PATH = Path(__file__).with_name("style_presets.json")
COMMON_FRAME_ANCHOR = (
    "Full-bleed 9:16 vertical single shot. NO border frames, NO split screen, "
    "NO multi-panel collage, NO subtitles, NO speech bubbles, NO watermark."
)
# Backward-compatible alias for callers that imported the legacy constant.
STYLE_LOCK = (
    "Art style: authentic 2D Korean webtoon manhwa anime animation. "
    "Crisp clean dark ink line art, vibrant flat cel-shaded coloring, "
    "authentic manhwa character features, controlled 2D animation. "
    "STRICTLY NOT 3D render, NOT live-action CGI, NOT photorealistic."
)


def load_style_profile(chapter_dir: Path, requested: str | None = None) -> tuple[str, dict]:
    """Load an explicit preset, or the chapter's style_selection.json."""
    config = json.loads(STYLE_CONFIG_PATH.read_text(encoding="utf-8"))
    candidates = [
        chapter_dir / "style_selection.json",
        chapter_dir.parent / "style_selection.json",
        chapter_dir.parent.parent / "style_selection.json",
    ]
    selection = next((p for p in candidates if p.exists()), None)
    selected = requested
    if not selected and selection and selection.exists():
        try:
            selected = json.loads(selection.read_text(encoding="utf-8")).get("default_preset")
        except Exception:
            selected = None
    presets = config.get("presets") or {}
    if not selected:
        available = ", ".join(sorted(presets))
        raise RuntimeError(
            f"No style preset provided and no style_selection.json found in {chapter_dir}. "
            f"Pass --style-preset <name>. Available presets: {available}"
        )
    if selected not in presets:
        available = ", ".join(sorted(presets))
        raise ValueError(f"Unknown style preset {selected!r}; choose one of: {available}")
    return selected, presets[selected]


def style_lines(profile: dict) -> list[str]:
    lines = [
        text(profile.get("style_anchor")),
        text(profile.get("motion_anchor")),
        text(profile.get("negative_anchor")),
        COMMON_FRAME_ANCHOR,
    ]
    ref_anchor = text(profile.get("reference_anchor"))
    if ref_anchor:
        lines.append(ref_anchor)
    return [line for line in lines if line]


def text(value: object) -> str:
    return " ".join(str(value or "").split())


def load_storyboard(chapter_dir: Path) -> tuple[dict, list[dict]]:
    source = chapter_dir / "storyboard_9_16.json"
    if not source.exists():
        raise FileNotFoundError(f"Missing canonical storyboard: {source}")
    data = json.loads(source.read_text(encoding="utf-8"))
    blocks = data.get("blocks") or []
    if not blocks:
        raise ValueError(f"No storyboard blocks in {source}")
    for number, block in enumerate(blocks, 1):
        beats = block.get("beats") or []
        if not beats:
            raise ValueError(f"Storyboard block {number} has no beats")
    return data, blocks


def format_shot_prompt(
    title: str,
    block: dict,
    beat: dict,
    block_number: int,
    beat_number: int,
    profile: dict,
    episode_context: str | None = None,
) -> str:
    final = beat_number == len(block.get("beats") or []) - 1
    header = (
        f"{episode_context}, beat {beat_number + 1}, timing {text(beat.get('timestamp'))}."
        if episode_context
        else f"Storyboard block {block_number}, beat {beat_number + 1}, timing {text(beat.get('timestamp'))}."
    )
    lines = [
        *style_lines(profile),
        f"Series: {text(title)}.",
        header,
        f"Create one continuous full-bleed shot for the beat labelled {text(beat.get('label'))}.",
        f"Action and composition: {text(beat.get('action'))}",
        f"Camera movement: {text(beat.get('camera'))}",
    ]
    if beat.get("vo"):
        lines.append(f"English dialogue or voiceover cue: {text(beat.get('vo'))}")
    if beat.get("sfx"):
        lines.append(f"Sound design suggestion: {text(beat.get('sfx'))}")
    if beat.get("page_file"):
        lines.append(
            f"Narrative source anchor: {text(beat.get('page_file'))}; preserve the scene, "
            "but do not reproduce the source page, gutters, captions, or scanlation text."
        )
    if final:
        lines.append(
            "END ON A COMPLETE FREEZE FRAME: the subject holds the final pose, eyes and "
            "hands still, with zero extra movement through the end of the block."
        )
    return "\n".join(line for line in lines if line.rstrip(": "))


def format_continuous_prompt(
    title: str,
    block: dict,
    block_number: int,
    profile: dict,
    episode_context: str | None = None,
) -> str:
    beats = block.get("beats") or []
    beat_lines = []
    for index, beat in enumerate(beats, 1):
        beat_lines.append(
            f"Beat {index} ({text(beat.get('timestamp'))}) — {text(beat.get('label'))}: "
            f"{text(beat.get('action'))} Camera: {text(beat.get('camera'))}."
        )
    block_target = (
        episode_context
        if episode_context
        else f"storyboard block {block_number}: {text(block.get('block_title'))}"
    )
    return "\n".join([
        *style_lines(profile),
        f"Series: {text(title)}.",
        f"Create one coherent 10-second vertical drama block, {block_target}.",
        "Maintain exact character identity, wardrobe, setting continuity, and chronological action across the beats.",
        *beat_lines,
        "Use the final beat as a complete freeze frame; do not add a new action after the final pose.",
    ])


def write_delimited(path: Path, prompts: list[str]) -> None:
    path.write_text(DELIMITER.join(prompt.strip() for prompt in prompts) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export storyboard blocks as plain-text prompts")
    parser.add_argument("--chapter-dir", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--style-preset", default=None, help="Style preset from style_presets.json; overrides chapter style_selection.json")
    args = parser.parse_args()

    chapter_dir = args.chapter_dir.resolve()
    output_dir = (args.output_dir or chapter_dir / "flow_queue").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    style_id, profile = load_style_profile(chapter_dir, args.style_preset)
    data, blocks = load_storyboard(chapter_dir)
    title = (
        data.get("title")
        or (
            json.loads((chapter_dir / "metadata.json").read_text(encoding="utf-8")).get("title")
            if (chapter_dir / "metadata.json").exists()
            else None
        )
        or (
            json.loads((chapter_dir.parent.parent / "metadata.json").read_text(encoding="utf-8")).get("title")
            if (chapter_dir.parent.parent / "metadata.json").exists()
            else None
        )
        or chapter_dir.name
    )
    all_shots: list[str] = []
    continuous: list[str] = []
    manifest = {
        "chapter_dir": str(chapter_dir),
        "format": "plain-text-prompts",
        "style_preset": style_id,
        "pacing_mode": data.get("pacing_mode", "single_episode"),
        "total_episodes": data.get("total_episodes", 1),
        "blocks": [],
    }

    has_episodes = bool(data.get("episodes") and len(data.get("episodes")) > 1)
    episode_prompts: dict[int, list[str]] = {}
    episode_continuous: dict[int, list[str]] = {}
    episode_manifests: dict[int, dict] = {}

    for block_number, block in enumerate(blocks, 1):
        ep_num = block.get("episode_number", 1)
        ep_block_num = block.get("episode_block_number", block_number)

        # Shot prompts for root flow_queue
        shots = [
            format_shot_prompt(title, block, beat, block_number, beat_number, profile)
            for beat_number, beat in enumerate(block.get("beats") or [])
        ]
        continuous_prompt = format_continuous_prompt(title, block, block_number, profile)

        # Shot prompts tailored for the specific episode (1-indexed per episode)
        ep_shots = [
            format_shot_prompt(
                title,
                block,
                beat,
                block_number,
                beat_number,
                profile,
                episode_context=f"Episode {ep_num}, storyboard block {ep_block_num}" if has_episodes else None,
            )
            for beat_number, beat in enumerate(block.get("beats") or [])
        ]
        ep_continuous_prompt = format_continuous_prompt(
            title,
            block,
            block_number,
            profile,
            episode_context=f"Episode {ep_num}, block {ep_block_num}: {text(block.get('block_title'))}" if has_episodes else None,
        )

        # Write root block prompt files
        write_delimited(output_dir / f"block{block_number}_prompts.txt", shots)
        (output_dir / f"block{block_number}_video_prompt.txt").write_text(
            continuous_prompt + "\n", encoding="utf-8"
        )

        # If multi-episode, also write epXX_blockN files in root and mirror into chapter_dir/episodes/epXX/flow_queue
        if has_episodes:
            write_delimited(output_dir / f"ep{ep_num:02d}_block{ep_block_num}_prompts.txt", ep_shots)
            (output_dir / f"ep{ep_num:02d}_block{ep_block_num}_video_prompt.txt").write_text(
                ep_continuous_prompt + "\n", encoding="utf-8"
            )
            episode_prompts.setdefault(ep_num, []).extend(ep_shots)
            episode_continuous.setdefault(ep_num, []).append(ep_continuous_prompt)

            ep_dir = chapter_dir / "episodes" / f"ep{ep_num:02d}" / "flow_queue"
            ep_dir.mkdir(parents=True, exist_ok=True)
            write_delimited(ep_dir / f"block{ep_block_num}_prompts.txt", ep_shots)
            (ep_dir / f"block{ep_block_num}_video_prompt.txt").write_text(
                ep_continuous_prompt + "\n", encoding="utf-8"
            )

            if ep_num not in episode_manifests:
                episode_manifests[ep_num] = {
                    "chapter_dir": str(chapter_dir / "episodes" / f"ep{ep_num:02d}"),
                    "episode_number": ep_num,
                    "format": "plain-text-prompts",
                    "style_preset": style_id,
                    "total_blocks": 0,
                    "total_shots": 0,
                    "blocks": [],
                }
            episode_manifests[ep_num]["total_blocks"] += 1
            episode_manifests[ep_num]["total_shots"] += len(ep_shots)
            episode_manifests[ep_num]["blocks"].append({
                "block": ep_block_num,
                "overall_block": block_number,
                "title": block.get("block_title"),
                "shot_count": len(ep_shots),
                "prompts_file": str(ep_dir / f"block{ep_block_num}_prompts.txt"),
                "continuous_file": str(ep_dir / f"block{ep_block_num}_video_prompt.txt"),
            })

        all_shots.extend(shots)
        continuous.append(continuous_prompt)
        manifest["blocks"].append({
            "block": block_number,
            "episode": ep_num,
            "episode_block": ep_block_num,
            "title": block.get("block_title"),
            "shot_count": len(shots),
            "prompts_file": str(output_dir / f"block{block_number}_prompts.txt"),
            "continuous_file": str(output_dir / f"block{block_number}_video_prompt.txt"),
        })

    # Write episode-level continuous and all-shots files if multi-part
    if has_episodes:
        for ep_num, ep_cont in episode_continuous.items():
            write_delimited(output_dir / f"ep{ep_num:02d}_flow_6_continuous_blocks.txt", ep_cont)
            ep_dir = chapter_dir / "episodes" / f"ep{ep_num:02d}" / "flow_queue"
            write_delimited(ep_dir / "flow_6_continuous_blocks.txt", ep_cont)
            write_delimited(ep_dir / f"flow_all_{len(episode_prompts[ep_num])}_shots.txt", episode_prompts[ep_num])
            if ep_num in episode_manifests:
                (ep_dir / "prompt_txt_manifest.json").write_text(
                    json.dumps(episode_manifests[ep_num], indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )

    write_delimited(output_dir / f"flow_{len(continuous)}_continuous_blocks.txt", continuous)
    write_delimited(output_dir / f"flow_all_{len(all_shots)}_shots.txt", all_shots)
    (output_dir / "prompt_txt_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"[OK] Wrote {len(blocks)} blocks ({manifest['total_episodes']} episodes) and {len(all_shots)} shot prompts to {output_dir}")


if __name__ == "__main__":
    main()
