#!/usr/bin/env python3
"""Generate finished Nano Banana SERYE storyboard sheets for Chapter 0."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

AGY = "/home/john/.local/bin/agy"


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def build_prompt(chapter: Path, block: dict, number: int, refs: list[Path], output: Path) -> str:
    title = "I'm the Max-Level Newbie"
    beats = block.get("beats") or []
    source_files = sorted({str(chapter / "images" / beat["page_file"]) for beat in beats})
    ref_files = "\n".join(str(p) for p in refs)
    positions = [
        "Beat 1 / Row 1 left",
        "Beat 2 / Row 1 right",
        "Beat 3 / Row 2 full width",
        "Beat 4 / Row 3 left and right, two distinct angles",
        "Beat 5 / Row 4 left and right, two distinct angles",
        "Beat 6 / Row 5 full width, final freeze frame",
    ]
    beat_lines = []
    for position, beat in zip(positions, beats):
        beat_lines.append(
            f"{position}: {clean(beat.get('timestamp'))} — {clean(beat.get('label'))}. "
            f"Visible action/composition: {clean(beat.get('action'))}. "
            f"Camera intention: {clean(beat.get('camera'))}."
        )
    return f"""Use Nano Banana Pro image generation. Create one finished professional SERYE drama director storyboard sheet for a 10-second vertical short-form video.

HEADER TEXT — render exactly in English:
SERYE DRAMA BLOCK — {title.upper()} —
Block {number} — {clean(block.get('block_title'))}

CANVAS AND COMPOSITION:
- Exact 9:16 vertical PNG, 768x1376 pixels.
- Solid matte black background and clean black gutters.
- EXACT 5-row grid with 8 distinct illustrated shots: Row 1 has 2 equal panels; Row 2 has 1 full-width cinematic panel; Row 3 has 2 equal panels; Row 4 has 2 equal panels; Row 5 has 1 full-width climactic panel.
- Place a small, crisp, readable white timestamp and all-caps English beat label in each panel's black caption strip. Use the exact timestamps and labels below.
- This must be a coherent director sheet, not a source-page collage and not a mechanical crop sheet.

CANONICAL SIX-BEAT DIRECTOR PLAN:
{chr(10).join(beat_lines)}

SHOT DIRECTION:
- Turn each beat into a newly staged, cinematic 2D Korean webtoon manhwa anime storyboard illustration. Do not paste, reproduce, or crop the source manga page.
- Panels 4 and 5 represent the same Beat 4 time window but must use two clearly different camera angles or compositions. Panels 6 and 7 represent the same Beat 5 time window but must also be distinct.
- Preserve exact character identity, face, hair, wardrobe, creature design, environment, action chronology, and color continuity from the attached local character reference sheets.
- Use deliberate shot grammar: establishing wide, medium/close reaction, dynamic action, extreme insert, opposing angle, and a final held hero pose.
- The final full-width Beat 6 panel must visibly read as the cliffhanger resolution and end on a complete freeze frame; no new action after the final pose.
- The source manga pages and references are visual guides only. Do not reproduce their gutters, scanlation credits, advertisements, speech bubbles, captions, Korean text, or watermarks.
- Do not render extra readable text inside artwork. Only the specified English header, timestamps, and beat labels may appear.

STYLE LOCK:
Authentic 2D Korean webtoon manhwa anime animation. Crisp clean dark ink line art, vibrant flat cel-shaded coloring, cinematic composition, authentic manhwa character features, fluid 2D animation design. STRICTLY NOT 3D render, NOT live-action CGI, NOT photorealistic, NOT western comic-book style. No watermark, no malformed text, no speech bubbles, no subtitles, no random logos, no storyboard inside the storyboard.

LOCAL NARRATIVE SOURCE PAGES:
{chr(10).join(source_files)}

LOCAL CHARACTER REFERENCE SHEETS — preserve these identities exactly:
{ref_files}

Save the finished generated PNG exactly here:
{output}
"""


def main() -> None:
    chapter = Path("/home/john/manga-reviews/output/im-the-max-level-newbie/ch0").resolve()
    storyboard_dir = chapter / "nano_storyboards"
    backup_dir = chapter / "nano_storyboards_crop_compositor"
    storyboard_dir.mkdir(parents=True, exist_ok=True)
    backup_dir.mkdir(parents=True, exist_ok=True)
    for old in sorted(storyboard_dir.glob("*.png")):
        target = backup_dir / old.name
        if target.exists():
            target.unlink()
        shutil.move(str(old), str(target))
    story = json.loads((chapter / "storyboard_9_16.json").read_text(encoding="utf-8"))
    refs = sorted((chapter / "character_refs").glob("*.png"))
    if not refs:
        raise SystemExit("No character references found")
    blocks = story.get("blocks") or []
    if len(blocks) != 6:
        raise SystemExit(f"Expected 6 blocks, found {len(blocks)}")
    for number, block in enumerate(blocks, 1):
        slug = "_".join(clean(block.get("block_title")).lower().split())
        output = storyboard_dir / f"block{number:02d}_{slug.replace(' ', '_')}.png"
        prompt = build_prompt(chapter, block, number, refs, output)
        print(f"[GENERATE] block {number}/6 -> {output}", flush=True)
        last_error = None
        for attempt in range(1, 3):
            try:
                result = subprocess.run(
                    [AGY, "--model", "gemini-3.8-flash-medium", "--effort", "medium", "--print-timeout", "15m", "-p", prompt],
                    capture_output=True, text=True, timeout=1000,
                )
                if result.returncode:
                    raise RuntimeError(result.stderr.strip() or f"agy exit {result.returncode}")
                if not output.exists():
                    raise RuntimeError("agy returned without creating the requested PNG")
                print(result.stdout.strip()[-500:], flush=True)
                break
            except Exception as exc:
                last_error = str(exc)
                print(f"[RETRY] block {number}, attempt {attempt}: {last_error}", flush=True)
        else:
            raise SystemExit(f"Block {number} failed: {last_error}")
    print(f"[COMPLETE] Generated {len(blocks)} Nano Banana storyboard sheets in {storyboard_dir}")


if __name__ == "__main__":
    main()
