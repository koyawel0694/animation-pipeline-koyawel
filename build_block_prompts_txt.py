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

from chapter_contract import script_cue


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

FLOW_POLICY_RULES = [
    # Restraint & human violence
    (r"\bforcefully pin(?:s|ned|ning)? down\b", "stand menacingly over"),
    (r"\bpin(?:s|ned|ning)? down\b", "stand over"),
    (r"\bpinned under\b", "trapped beneath"),
    
    # Human blood, spitting, weeping blood
    (r"\bweeping and coughing up a stream of dark blood\b", "breathing heavily in exhaustion amidst dark industrial soot"),
    (r"\bcoughing up a stream of dark blood\b", "coughing heavily amidst dark industrial soot"),
    (r"\bweeping blood\b", "breathing heavily in exhaustion"),
    (r"\bspitting blood\b", "breathing heavily in exhaustion"),
    (r"\bcoughed up blood\b", "gasped for breath amidst soot"),
    (r"\btear-streaked face stained with blood\b", "tense, determined face marked with dark quarry soot"),
    
    # Impalement and extreme gore
    (r"\bimpales? directly through the protagonist\'s back and torso\b", "strikes powerfully against the protagonist, knocking him down"),
    (r"\bimpales? straight through the supervisor\'s chest from behind\b", "strikes down against the supervisor from behind in a sudden ambush"),
    (r"\bimpales? (?:directly |straight )?through\b", "strikes forcefully against"),
    (r"\bimpaled protagonist\b", "recoiling protagonist"),
    (r"\bimpaled\b", "struck down"),
    (r"\bpierces? straight through the supervisor\'s chest from behind\b", "strikes down against the supervisor from behind in a sudden ambush"),
    (r"\bpierces? straight through\b", "strikes forcefully against"),
    (r"\bpierces?\b", "strikes"),
    
    # Agony, limp body, gore details
    (r"\bhoists the limp protagonist into the air by the back of his neck and head[^\n,;]*", "looms overpoweringly above the fallen protagonist in the dark quarry"),
    (r"\bhoists the limp protagonist into the air\b", "towers overpoweringly over the fallen protagonist"),
    (r"\blimp protagonist\b", "exhausted protagonist"),
    (r"\bbroken body\b", "weary frame"),
    (r"\bexcruciating agony\b", "overwhelming shock and strain"),
    (r"\bscreaming as blood splatters across the arena\b", "shouting as dark kinetic shockwaves ripple across the ground"),
    
    # Blood & splatters
    (r"\bblood splatters? across the dark rock\b", "dark dust and debris scatter across the dark rock"),
    (r"\bblood splatters? across the arena\b", "dark shockwaves scatter across the ground"),
    (r"\bblood splatters?\b", "dark shadow particles"),
    (r"\bblood drips? from his body\b", "dark shadow motes drift from his silhouette"),
    (r"\bblood drips?\b", "dark motes drift"),
    (r"\bstream of dark blood\b", "dark shadow motes"),
    (r"\bbloodshot eye surrounded by crimson blood splatter\b", "wide strained eye surrounded by high-contrast shadowy particles"),
    (r"\bbloodshot\b", "strained, intense"),
    (r"\bbattered and bloodied\b", "battered and soot-covered"),
    (r"\bbloodied\b", "soot-covered"),
    (r"\bbleeding protagonist\'s face\b", "exhausted protagonist\'s face"),
    (r"\bbleeding\b", "exhausted"),
    (r"\bstained with blood\b", "marked with dark quarry soot"),
    (r"\bblood on (?:his|her|their) knuckles\b", "dark grime on their knuckles"),
    (r"\bblood\b", "dark soot smudges"),
    (r"\bbloody\b", "shadowy"),
    
    # Crying / weeping / grief
    (r"\btear-streaked face\b", "tense, soot-stained face"),
    (r"\btear-streaked\b", "sweat-stained"),
    (r"\btears on skin\b", "sweat on skin"),
    (r"\bweeping\b", "grimacing in pain"),
    (r"\bcrying out in despair\b", "calling out in defiance"),
    (r"\bcrying\b", "grimacing with exertion"),
    (r"\bsobbing\b", "gasping for air"),
    
    # Slaughter / corpses
    (r"\bslaughter\b", "frenzied clash"),
    (r"\bcorpses?\b", "fallen silhouettes"),
    (r"\bdead bodies\b", "fallen silhouettes"),
    (r"\bdead miners?\b", "fallen miners"),
    (r"\bdeadliness\b", "lethal danger"),
    (r"\bkill(?:ing)?\b", "overpowering"),
]


def sanitize_flow_action(text: str) -> str:
    """Soft-revise action and camera text to comply with Google Flow safety policies."""
    for pattern, replacement in FLOW_POLICY_RULES:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


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
            selection_data = json.loads(selection.read_text(encoding="utf-8"))
            selected = selection_data.get("default_preset")
            confirmed = selection_data.get("selected_by_user") is True or selection_data.get("selection_method") in {
                "cli_override",
                "interactive",
                "clarify",
            }
            if not confirmed:
                raise RuntimeError(
                    f"Style selection in {selection} is provisional. Ask the user to choose a style "
                    "or pass --style-preset explicitly before generating prompts."
                )
        except (OSError, json.JSONDecodeError, TypeError):
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


def extract_characters_for_beats(beats: list[dict], chapter_dir: Path | None = None) -> list[str]:
    """Extract and normalize prominent character names for prompt headers."""
    known = []
    if chapter_dir:
        char_paths = [
            chapter_dir / "characters.json",
            chapter_dir.parent / "characters.json",
            chapter_dir.parent.parent / "characters.json",
        ]
        for p in char_paths:
            if p.exists():
                try:
                    cdata = json.loads(p.read_text(encoding="utf-8"))
                    for item in cdata:
                        raw_name = item.get("name", "")
                        slug = item.get("slug", "")
                        clean_name = re.sub(r"\(.*?\)", "", raw_name).strip()
                        clean_name = " ".join(w.capitalize() for w in clean_name.split())
                        if clean_name:
                            known.append((clean_name, slug.lower() if slug else "", raw_name.lower()))
                    if known:
                        break
                except Exception:
                    pass

    text_corpus = " ".join(
        f"{b.get('speaker', '')} {b.get('action', '')} {b.get('scene_title', '')} {b.get('vo', '')}"
        for b in beats
    ).lower()

    found = []
    for display_name, slug, full_name in known:
        slug_words = [w for w in slug.split("_") if len(w) > 2]
        if (
            display_name.lower() in text_corpus
            or (slug and slug in text_corpus)
            or any(w in text_corpus for w in slug_words)
            or (display_name == "Li Yi" and any(w in text_corpus for w in ["li yi", "protagonist"]))
            or ("shadow beast" in display_name.lower() and any(w in text_corpus for w in ["shadow beast", "alien predator", "alien creature", "alien beast", "alien"]))
        ):
            found.append(display_name)

    for b in beats:
        spk = b.get("speaker", "").strip()
        clean_spk = re.sub(r"\(.*?\)", "", spk).strip()
        if clean_spk and clean_spk.lower() not in {"narrator", "sfx", "sound effect", "system", "caption", "none", "unknown", "protagonist"}:
            title_spk = " ".join(w.capitalize() for w in clean_spk.split())
            if "miner" in title_spk.lower() or "worker" in title_spk.lower():
                title_spk = "Miners"
            elif "supervisor" in title_spk.lower():
                title_spk = "Supervisor Chen"
            elif "alien" in title_spk.lower() or "beast" in title_spk.lower():
                title_spk = "Otherworld Shadow Beast"
            if not any(title_spk.lower() == f.lower() for f in found):
                found.append(title_spk)

    seen = set()
    result = []
    for c in found:
        if c.lower() not in seen:
            seen.add(c.lower())
            result.append(c)
    return result or ["Li Yi"]


def format_shot_prompt(
    title: str,
    block: dict,
    beat: dict,
    block_number: int,
    beat_number: int,
    profile: dict,
    episode_context: str | None = None,
    chapter_dir: Path | None = None,
) -> str:
    final = beat_number == len(block.get("beats") or []) - 1
    header = (
        f"{episode_context}, beat {beat_number + 1}, timing {text(beat.get('timestamp'))}."
        if episode_context
        else f"Storyboard block {block_number}, beat {beat_number + 1}, timing {text(beat.get('timestamp'))}."
    )
    characters = extract_characters_for_beats([beat], chapter_dir) or extract_characters_for_beats(block.get("beats") or [], chapter_dir)
    char_header = f"(Characters: {', '.join(characters)})" if characters else ""
    lines = []
    if char_header:
        lines.append(char_header)
    lines.extend([
        *style_lines(profile),
        f"Series: {text(title)}.",
        header,
        f"Create one continuous full-bleed shot for the beat labelled {text(beat.get('label'))}.",
        f"Canonical source scene: {text(beat.get('source_scene_id'))} — {sanitize_flow_action(text(beat.get('scene_title')))}.",
        f"Action and composition: {sanitize_flow_action(text(beat.get('action')))}",
        f"Camera movement: {sanitize_flow_action(text(beat.get('camera')))}",
        script_cue(beat),
    ])
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
    chapter_dir: Path | None = None,
) -> str:
    characters = extract_characters_for_beats(block.get("beats") or [], chapter_dir)
    char_header = f"(Characters: {', '.join(characters)})" if characters else ""
    beats = block.get("beats") or []
    beat_lines = []
    for index, beat in enumerate(beats, 1):
        beat_lines.append(
            f"Beat {index} ({text(beat.get('timestamp'))}) — {text(beat.get('label'))}: "
            f"Canonical source scene {text(beat.get('source_scene_id'))} ({sanitize_flow_action(text(beat.get('scene_title')))}). "
            f"{sanitize_flow_action(text(beat.get('action')))} Camera: {sanitize_flow_action(text(beat.get('camera')))}. "
            f"{script_cue(beat)}"
        )
    block_target = (
        episode_context
        if episode_context
        else f"storyboard block {block_number}: {sanitize_flow_action(text(block.get('block_title')))}"
    )
    lines = []
    if char_header:
        lines.append(char_header)
    lines.extend([
        *style_lines(profile),
        f"Series: {text(title)}.",
        f"Create one coherent 10-second vertical drama block, {block_target}.",
        "Maintain exact character identity, wardrobe, setting continuity, and chronological action across the beats.",
        "Use only the exact manga script cues below. Do not invent, paraphrase, repeat, or move dialogue between beats.",
        *beat_lines,
        "Use the final beat as a complete freeze frame; do not add a new action after the final pose.",
    ])
    return "\n".join(lines)


def write_delimited(path: Path, prompts: list[str]) -> None:
    path.write_text(DELIMITER.join(prompt.strip() for prompt in prompts) + "\n", encoding="utf-8")


def clean_managed_prompt_files(output_dir: Path) -> None:
    """Remove only files owned by this exporter before a deterministic rebuild."""
    patterns = (
        "block*_prompts.txt",
        "block*_video_prompt.txt",
        "ep??_block*_prompts.txt",
        "ep??_block*_video_prompt.txt",
        "ep??_flow_6_continuous_blocks.txt",
        "flow_*_continuous_blocks.txt",
        "flow_all_*_shots.txt",
        "prompt_txt_manifest.json",
    )
    for pattern in patterns:
        for path in output_dir.glob(pattern):
            if path.is_file():
                path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Export storyboard blocks as plain-text prompts")
    parser.add_argument("--chapter-dir", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--style-preset", default=None, help="Style preset from style_presets.json; overrides chapter style_selection.json")
    args = parser.parse_args()

    chapter_dir = args.chapter_dir.resolve()
    output_dir = (args.output_dir or chapter_dir / "flow_queue").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    script_path = chapter_dir / "chapter_script.json"
    if not script_path.exists():
        raise FileNotFoundError(
            f"Missing canonical chapter script: {script_path}; run build_serye_storyboard.py first"
        )
    style_id, profile = load_style_profile(chapter_dir, args.style_preset)
    data, blocks = load_storyboard(chapter_dir)
    clean_managed_prompt_files(output_dir)
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
        "script_artifact": str((chapter_dir / "chapter_script.json").resolve()) if (chapter_dir / "chapter_script.json").exists() else None,
        "pacing_mode": data.get("pacing_mode", "single_episode"),
        "total_episodes": data.get("total_episodes", 1),
        "blocks": [],
    }

    has_episodes = bool(data.get("episodes") and len(data.get("episodes")) > 1)
    episode_prompts: dict[int, list[str]] = {}
    episode_continuous: dict[int, list[str]] = {}
    episode_manifests: dict[int, dict] = {}
    if has_episodes:
        for episode in data.get("episodes") or []:
            ep_num = episode.get("episode_number", 1)
            ep_dir = chapter_dir / "episodes" / f"ep{ep_num:02d}" / "flow_queue"
            ep_dir.mkdir(parents=True, exist_ok=True)
            clean_managed_prompt_files(ep_dir)

    for block_number, block in enumerate(blocks, 1):
        ep_num = block.get("episode_number", 1)
        ep_block_num = block.get("episode_block_number", block_number)

        # Shot prompts for root flow_queue
        shots = [
            format_shot_prompt(title, block, beat, block_number, beat_number, profile, chapter_dir=chapter_dir)
            for beat_number, beat in enumerate(block.get("beats") or [])
        ]
        continuous_prompt = format_continuous_prompt(title, block, block_number, profile, chapter_dir=chapter_dir)

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
                chapter_dir=chapter_dir,
            )
            for beat_number, beat in enumerate(block.get("beats") or [])
        ]
        ep_continuous_prompt = format_continuous_prompt(
            title,
            block,
            block_number,
            profile,
            episode_context=f"Episode {ep_num}, block {ep_block_num}: {text(block.get('block_title'))}" if has_episodes else None,
            chapter_dir=chapter_dir,
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
                    "script_artifact": str((chapter_dir / "episodes" / f"ep{ep_num:02d}" / "chapter_script.json").resolve()),
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
