#!/usr/bin/env python3
"""Generate Nano Banana Pro character sheets and SERYE storyboard sheets through agy."""
import argparse
import json
import subprocess
import time
import re
from pathlib import Path

AGY = "/home/john/.local/bin/agy"


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
        specs.append((f"block{index:02d}_{slugify(title)}", f"Block {index} — {title}", page_files, labels))
    if not specs:
        raise ValueError(f"No storyboard blocks found in {storyboard_path}")
    return specs


def chapter_paths(chapter_dir: Path, reference_dir: Path | None = None):
    return chapter_dir, reference_dir or chapter_dir / "character_refs", chapter_dir / "nano_storyboards"


def validate_reference_dir(reference_dir: Path):
    refs = sorted(reference_dir.glob("*.png"))
    if not refs:
        raise FileNotFoundError(f"No character reference PNGs found in {reference_dir}")
    return refs


def copy_reference_manifest(reference_dir: Path, chapter_dir: Path):
    """Record reused refs without duplicating or regenerating PNGs."""
    manifest = chapter_dir / "character_refs_source.json"
    manifest.write_text(json.dumps({
        "source_dir": str(reference_dir),
        "files": [str(path) for path in validate_reference_dir(reference_dir)],
        "reused": True,
    }, indent=2), encoding="utf-8")
    return manifest


CHARACTERS = [
    ("kang_jin_hoo", "KANG JIN-HOO", "23-year-old Korean man, recently discharged military veteran, lean athletic build, fair skin, short tousled black hair with textured bangs, sharp tired intelligent dark eyes, defined jawline, restrained understated expression. Wardrobe anchor: cream long-sleeve crewneck shirt, dark indigo jeans, white low-top sneakers. Include front full-body, 3/4 portrait, side profile, seated casual pose."),
    ("oh_taek_gyu", "OH TAEK-GYU", "23-year-old Korean man, stocky build, round friendly face, short dark hair, thick black-rimmed glasses, expressive eyebrows, casual energetic personality. Wardrobe anchor: gray zip-up hoodie over white T-shirt, dark casual trousers, sneakers. Include front full-body, 3/4 portrait, side profile, seated pose holding a small device or game collectible."),
    ("street_reporter", "STREET REPORTER", "Young Korean male television street reporter, slim build, neat side-parted black hair, sharp friendly face, expressive dark eyes. Wardrobe anchor: tailored charcoal-gray suit, crisp white shirt, black tie, handheld blue broadcast microphone. Include front full-body, 3/4 portrait, side profile, microphone pose."),
    ("shin_yuri", "SHIN YURI", "Young Korean woman, elegant and confident, long wavy honey-blonde hair, warm expressive eyes, fair skin, charming intelligent smile. Wardrobe anchor: refined beige blouse, simple crossbody strap, understated professional styling. Include front full-body, 3/4 portrait, side profile, interview pose."),
    ("female_interviewer", "FEMALE INTERVIEWER", "Young Korean woman, poised professional broadcast interviewer, neatly styled dark chin-length bob, refined facial features, calm inquisitive eyes. Wardrobe anchor: tailored navy blue blazer, dark blouse, interview cue cards. Include front full-body, 3/4 portrait, side profile, seated interview pose."),
    ("spirit_shaman", "SPIRIT SHAMAN AND FLAMING EAGLE", "Supernatural Korean shamanic spirit with an aged expressive face, ornate traditional ceremonial headdress, layered green and gold ritual robes, pale glowing eyes, surrounded by controlled emerald mist. Include a separate flaming eagle manifestation: realistic bald eagle with outstretched wings, radiant golden-pink flame aura, physically detailed feathers. Clearly separate human spirit and eagle forms in one reference sheet."),
]

BLOCKS = [
    ("block01_the_question", "Block 1 — The Question That Changes Everything", ["page_001.webp", "page_002.webp"], ["Street Interview Opening", "The Hundred Million Won Question", "The Slothful Dream", "The Ultimate Hypothetical Question", "The Final Question", "The Realistic Inquiry"]),
    ("block02_the_richest_man", "Block 2 — The Man Who Became Richest", ["page_003.webp", "page_004.webp", "page_005.webp"], ["Interview with the World's Richest Person", "Rumors of Clairvoyance", "Casual Denial", "Sudden Activation of the Golden Eye", "Apparition in the Studio", "Golden Gaze and Smirk"]),
    ("block03_before_the_fortune", "Block 3 — Before the Fortune", ["page_006.webp", "page_007.webp", "page_008.webp", "page_009.webp", "page_010.webp"], ["Waking Up Groggy", "The Discharge Cap", "The Semi-Basement Apartment", "Remnants of Family Prosperity", "Introducing Oh Taek-Gyu", "The Bantcoin Encryption Key"]),
    ("block04_thirteen_billion", "Block 4 — Thirteen Point Five Billion Won", ["page_010.webp", "page_011.webp", "page_012.webp", "page_013.webp", "page_014.webp"], ["The Price Quote", "The Unit Clarification", "The Staggering Reality", "13.5 Billion Won", "Shameless Request", "The Spark of Memory"]),
    ("block05_warning_tomorrow", "Block 5 — The Warning From Tomorrow", ["page_015.webp", "page_016.webp", "page_017.webp", "page_018.webp"], ["Aura of the Flaming Eagle", "Recurrence of the Vision", "Fiery Inscription", "Inquiring About Mountainhill", "The Fiery Warning", "Sell All Your Bantcoin"]),
    ("block06_future_real", "Block 6 — The Future Is Real", ["page_019.webp", "page_020.webp", "page_021.webp", "page_022.webp", "page_023.webp"], ["Taek-Gyu Agrees to Liquidate", "Server Down", "The Empty Accounts Revelation", "Community Panic and Uproar", "The Revelation", "Website Promotional End Card"]),
]


def run(prompt, timeout=900):
    result = subprocess.run([AGY, "--model", "gemini-3.8-flash-medium", "--effort", "medium", "--print-timeout", "15m", "-p", prompt], capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"agy exit {result.returncode}")
    return result.stdout.strip()


def make_character_prompt(name, details, out):
    return f"""Use Nano Banana Pro image generation. Generate a professional vertical 9:16 character reference sheet for {name}.

CHARACTER DESIGN LOCK:
{details}

Layout: one clean 9:16 sheet on off-white studio background. Show exactly four consistent views: front full body, 3/4 portrait, side profile, seated or action pose. Repeat same face, hair, age, body proportions, and wardrobe in every view. Add a small readable header with the character name and a tiny wardrobe note. Crisp premium modern digital manhwa/webtoon art, realistic anatomy, clean linework, controlled cell shading, professional model sheet. No plot scene, no extra characters, no speech bubbles, no watermark, no story panels, no collage borders beyond the sheet layout.
Save generated PNG exactly here: {out}
"""


def make_storyboard_prompt(title, panel_files, labels, out, chapter_dir, ref_dir, manga_title):
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

CANVAS AND GRID — FOLLOW EXACTLY:
- 9:16 vertical, approximately 768x1376 pixels.
- Premium commercial modern manhwa/webtoon art, crisp linework, realistic anatomy, controlled cell shading.
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
    args = ap.parse_args()
    base, ref_dir, sb_dir = chapter_paths(args.chapter_dir.resolve(), args.reference_dir)
    if args.reference_dir:
        copy_reference_manifest(ref_dir, base)
    ref_dir.mkdir(parents=True, exist_ok=True)
    sb_dir.mkdir(parents=True, exist_ok=True)
    if not (args.characters or args.storyboards or args.all):
        ap.error("choose --characters, --storyboards, or --all")

    metadata = {}
    metadata_path = base / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    manga_title = metadata.get("title") or "Manga Chapter"

    if (args.characters or args.all) and not args.reference_dir:
        for slug, name, details in CHARACTERS:
            out = ref_dir / f"{slug}_ref.png"
            print(f"[CHARACTER] {name} -> {out}", flush=True)
            run(make_character_prompt(name, details, out))
            print("[OK]", flush=True)
    elif args.reference_dir:
        print(f"[CHARACTER] Reusing existing refs from {ref_dir}", flush=True)
        validate_reference_dir(ref_dir)

    if args.storyboards or args.all:
        for slug, title, pages, labels in build_block_specs(base):
            out = sb_dir / f"{slug}.png"
            print(f"[STORYBOARD] {title} -> {out}", flush=True)
            run(make_storyboard_prompt(title, pages, labels, out, base, ref_dir, manga_title))
            print("[OK]", flush=True)

if __name__ == "__main__":
    main()
