#!/usr/bin/env python3
"""Generate Nano Banana Pro character sheets and SERYE storyboard sheets through agy."""
import argparse
import json
import os
import subprocess
import sys
import time
import re
from pathlib import Path

from PIL import Image

AGY = os.environ.get("AGY_BIN", "/home/john/.local/bin/agy")
STYLE_CONFIG_PATH = Path(__file__).with_name("style_presets.json")


def load_style_profile(chapter_dir: Path, requested: str | None = None) -> tuple[str, dict]:
    """Load an explicit, confirmed preset; never silently fall back."""
    if not STYLE_CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing style preset configuration: {STYLE_CONFIG_PATH}")
    config = json.loads(STYLE_CONFIG_PATH.read_text(encoding="utf-8"))
    selection = chapter_dir / "style_selection.json"
    selected = requested
    if not selected and selection.exists():
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
                    "or pass --style-preset explicitly before generating assets."
                )
        except (OSError, json.JSONDecodeError, TypeError):
            selected = None
    presets = config.get("presets", {})
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


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return value or "untitled"


def build_block_specs(chapter_dir: Path):
    """Build visual blocks from canonical storyboard JSON for this chapter."""
    storyboard_path = chapter_dir / "storyboard_9_16.json"
    if not storyboard_path.exists():
        raise FileNotFoundError(
            f"Missing {storyboard_path}; build storyboard metadata before visual assets"
        )

    data = json.loads(storyboard_path.read_text(encoding="utf-8"))
    specs = []
    for index, block in enumerate(data.get("blocks", []), start=1):
        title = block.get("block_title", f"Block {index}")
        beats = block.get("beats", [])
        page_files = []
        labels = []
        for beat in beats:
            page_file = beat.get("page_file")
            if page_file and page_file not in page_files:
                page_files.append(page_file)
            labels.append(beat.get("label", f"BEAT {len(labels) + 1}"))
        if not page_files:
            raise ValueError(f"Storyboard block {index} has no source page files")

        ep_num = block.get("episode_number")
        ep_block = block.get("episode_block_number")
        if ep_num is not None and ep_block is not None and data.get("total_episodes", 1) > 1:
            slug_prefix = f"ep{ep_num:02d}_block{ep_block:02d}"
            label_prefix = f"Part {ep_num} Block {ep_block}"
        else:
            slug_prefix = f"block{index:02d}"
            label_prefix = f"Block {index}"

        specs.append((f"{slug_prefix}_{slugify(title)}", f"{label_prefix} — {title}", page_files, labels))
    if not specs:
        raise ValueError(f"No storyboard blocks found in {storyboard_path}")
    return specs


def chapter_paths(chapter_dir: Path, reference_dir: Path | None = None):
    return chapter_dir, reference_dir or chapter_dir / "character_refs", chapter_dir / "nano_storyboards"


def validate_reference_dir(reference_dir: Path):
    refs = sorted(reference_dir.glob("*.png"))
    if not refs:
        raise FileNotFoundError(f"No character reference PNGs found in {reference_dir}")
    for path in refs:
        try:
            with Image.open(path) as image:
                if image.size != (768, 1376):
                    raise ValueError(f"reference must be 768x1376, got {image.size}")
                image.verify()
        except Exception as exc:
            raise ValueError(f"Invalid character reference {path}: {exc}") from exc
    return refs


def write_reference_manifest(
    reference_dir: Path,
    chapter_dir: Path,
    reused: bool,
    style_preset: str,
) -> Path:
    """Record the exact reference origin for both new and reused refs."""
    manifest = chapter_dir / "character_refs_source.json"
    metadata = {}
    metadata_path = chapter_dir / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    manifest.write_text(json.dumps({
        "source_dir": str(reference_dir.resolve()),
        "files": [str(path.resolve()) for path in validate_reference_dir(reference_dir)],
        "reused": reused,
        "series": metadata.get("series_slug") or metadata.get("title"),
        "chapter": str((metadata.get("chapter") or {}).get("chapter", metadata.get("chapter", "")))
        if isinstance(metadata.get("chapter"), dict) else str(metadata.get("chapter", "")),
        "style_preset_at_generation": style_preset,
        "status": "reused_canonical_refs" if reused else "canonical_character_refs",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def copy_reference_manifest(reference_dir: Path, chapter_dir: Path, style_preset: str = ""):
    """Record reused refs without duplicating or regenerating PNGs."""
    return write_reference_manifest(reference_dir, chapter_dir, reused=True, style_preset=style_preset)

def load_characters(chapter_dir: Path, characters_file: Path | None = None) -> list[tuple[str, str, str]]:
    """Load chapter- or series-specific character definitions from characters.json."""
    paths_to_check = []
    if characters_file:
        paths_to_check.append(characters_file)
    paths_to_check.extend([
        chapter_dir / "characters.json",
        chapter_dir.parent / "characters.json",
    ])
    for p in paths_to_check:
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                result = []
                for item in data:
                    slug = item.get("slug")
                    name = item.get("name")
                    details = item.get("details")
                    if slug and name and details:
                        result.append((slug, name, details))
                if result:
                    return result
            except Exception as e:
                print(f"[WARN] Failed to parse {p}: {e}", file=sys.stderr)
    raise RuntimeError(
        f"No chapter-specific characters.json found for {chapter_dir}. "
        "Refusing to guess character identities; provide canonical character definitions before generation."
    )

def run(prompt, timeout=900):
    result = subprocess.run([AGY, "--model", "gemini-3.8-flash-medium", "--effort", "medium", "--print-timeout", "15m", "-p", prompt], capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"agy exit {result.returncode}")
    return result.stdout.strip()


def make_character_prompt(name, details, out, profile: dict | None = None):
    profile = profile or {}
    char_style = profile.get(
        "character_ref_style",
        "Art style: authentic 2D Korean webtoon manhwa anime animation. Crisp clean dark ink line art, vibrant flat cel-shaded coloring, authentic manhwa character features, professional model sheet."
    )
    negative = profile.get("negative_anchor", "STRICTLY NOT 3D render, NOT live action, NOT photorealistic.")
    return f"""Use Nano Banana Pro image generation. Generate a professional vertical 9:16 character reference sheet for {name}.

CHARACTER DESIGN LOCK:
{details}

STYLE DIRECTIVES:
{char_style}
Negative constraints: {negative}

Layout: one clean 9:16 sheet on neutral studio background. Show exactly four consistent turnaround views: front full body, 3/4 portrait, side profile, and action pose. Repeat same face, hair, age, body proportions, and wardrobe in every view. Add a small readable header banner with the character name and a tiny wardrobe note. Professional model sheet. No plot scene, no extra characters, no speech bubbles, no watermark, no story panels, no collage borders beyond the sheet layout.
Save generated PNG exactly here: {out}
"""


def make_storyboard_prompt(title, panel_files, labels, out, chapter_dir, ref_dir, manga_title, profile: dict | None = None):
    profile = profile or {}
    sb_style = profile.get(
        "storyboard_style",
        "Visual style: authentic 2D Korean webtoon manhwa director sheet. Crisp dark ink lines, vibrant cel shading."
    )
    sb_neg = profile.get(
        "negative_anchor",
        "STRICTLY NOT 3D render, NOT live-action CGI, NOT photorealistic, no watermark."
    )
    ref_paths = "\n".join(str(p) for p in sorted(ref_dir.glob("*.png")))
    panels = "\n".join(f"{i+1}. {label} ({panel_files[min(i, len(panel_files)-1)]})" for i, label in enumerate(labels))
    timestamp_lines = "\n".join([
        "Beat 1 / Row 1 left: 0s-1.5s — label: THE OPENING",
        "Beat 2 / Row 1 right: 1.5s-3s — label: THE TURN",
        "Beat 3 / Row 2 full width: 3s-4.5s — label: THE REACTION",
        "Beat 4 / Row 3 left+right split: 4.5s-6s — label across seam: THE ESCALATION",
        "Beat 5 / Row 4 left+right split: 6s-8s — label across seam: THE REVEAL",
        "Beat 6 / Row 5 full width: 8s-10s — label: THE REVELATION — END ON FREEZE FRAME",
    ])
    return f"""Use Nano Banana Pro image generation. Create one finished visual storyboard sheet for a 10-second vertical short-form video.

HEADER TEXT exactly:
SERYE DRAMA BLOCK — {manga_title} — {title}

STYLE AND FORMAT:
- {sb_style}
- Constraints: {sb_neg}

CANVAS AND GRID — FOLLOW EXACTLY:
- 9:16 vertical, approximately 768x1376 pixels.
- Solid black title banner at top with small bold white header.
- Solid black gutters between panels and rows.
- EXACT GRID: Row 1 = two equal panels side by side. Row 2 = one full-width panel. Row 3 = two equal panels side by side. Row 4 = two equal panels side by side. Row 5 = one full-width final panel.
- Exactly 8 distinct visual shots total: 2 + 1 + 2 + 2 + 1. Do not duplicate a shot. Do not add panels.

EXACT TIMING AND LABELS — render every label clearly in bold white all-caps with black outline:
{timestamp_lines}

STORYBOARD BEATS:
{panels}

CANONICAL SOURCE PANEL FILES:
{chr(10).join(str(chapter_dir / 'images' / x) for x in panel_files)}

CHARACTER REFERENCE SHEETS — READ THESE LOCAL PNG FILES AND PRESERVE EXACT FACES, HAIR, body proportions, and wardrobe whenever characters appear:
{ref_paths}

DIRECTOR RULES:
- One coherent chronological dramatic progression across six beats; do not make a random montage.
- Every split panel must show a different camera shot or reaction, never duplicate artwork.
- Use clear visual compositions: establishing shot, close-up, hero shot, reaction shot, macro insert, final wide.
- Use only facts from this chapter's canonical analysis. Do not introduce unrelated genres, website advertisements, aggregator logos, or promotional end cards.
- All visible labels, captions, and rendered text must be natural English. Do not render Korean, Chinese, or other non-English text.
- Do not show phones, computer screens, trading charts, documents, or signs with readable paragraphs. If a screen or UI appears, show abstract shapes only; no invented words.
- Preserve exact character continuity from reference sheets. No hair-color changes, wardrobe changes, face swaps, or extra characters.
- Labels must be short, exactly as specified above, and each visual beat must have its own visible timestamp or shared seam label. Do not omit any timestamp.
- Final full-width panel: use actual chapter characters and setting, explicit held pose, no new motion, designed as freeze frame for Google Flow planning.
- No watermark, no random logos, no malformed text, no storyboard inside storyboard, no white pillarbox margins.

Save generated PNG exactly here: {out}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter-dir", required=True, type=Path)
    ap.add_argument("--reference-dir", type=Path, default=None,
                    help="Existing character refs to reuse; no regeneration")
    ap.add_argument("--characters", action="store_true")
    ap.add_argument("--storyboards", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--style-preset", default=None, help="Art style preset from style_presets.json")
    ap.add_argument("--characters-file", type=Path, default=None, help="Path to characters.json definition file")
    args = ap.parse_args()
    base, ref_dir, sb_dir = chapter_paths(args.chapter_dir.resolve(), args.reference_dir)
    ref_dir.mkdir(parents=True, exist_ok=True)
    sb_dir.mkdir(parents=True, exist_ok=True)
    if not (args.characters or args.storyboards or args.all):
        ap.error("choose --characters, --storyboards, or --all")

    selected_style, profile = load_style_profile(base, args.style_preset)
    print(f"[STYLE] Active art style preset: {selected_style} ({profile.get('label', '')})", flush=True)

    selection_path = base / "style_selection.json"
    if args.style_preset or not selection_path.exists():
        selection_path.write_text(json.dumps({
            "default_preset": selected_style,
            "label": profile.get("label", ""),
            "selected_by_user": True,
            "selection_method": "cli_override" if args.style_preset else "interactive",
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }, indent=2) + "\n", encoding="utf-8")

    metadata = {}
    metadata_path = base / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    manga_title = metadata.get("title") or "Manga Chapter"

    if (args.characters or args.all) and not args.reference_dir:
        active_characters = load_characters(base, args.characters_file)
        for slug, name, details in active_characters:
            out = ref_dir / f"{slug}_ref.png"
            print(f"[CHARACTER] {name} -> {out} [{selected_style}]", flush=True)
            run(make_character_prompt(name, details, out, profile))
            validate_reference_dir(ref_dir)
            print("[OK]", flush=True)
        write_reference_manifest(ref_dir, base, reused=False, style_preset=selected_style)
    elif args.reference_dir:
        print(f"[CHARACTER] Reusing existing refs from {ref_dir}", flush=True)
        validate_reference_dir(ref_dir)
        write_reference_manifest(ref_dir, base, reused=True, style_preset=selected_style)

    if args.storyboards or args.all:
        validate_reference_dir(ref_dir)
        for slug, title, pages, labels in build_block_specs(base):
            out = sb_dir / f"{slug}.png"
            print(f"[STORYBOARD] {title} -> {out} [{selected_style}]", flush=True)
            run(make_storyboard_prompt(title, pages, labels, out, base, ref_dir, manga_title, profile))
            try:
                with Image.open(out) as image:
                    if image.size != (768, 1376):
                        raise ValueError(f"storyboard must be 768x1376, got {image.size}")
                    image.verify()
            except Exception as exc:
                raise RuntimeError(f"Generated storyboard is invalid: {out}: {exc}") from exc
            print("[OK]", flush=True)

if __name__ == "__main__":
    main()
