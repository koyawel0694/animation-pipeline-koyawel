#!/usr/bin/env python3
"""Build full 30-file Flow Automator Max V3 production suite for Chapter 2."""
import csv
import json
from pathlib import Path

BASE = Path('/home/john/manga-reviews/output/the-investor-who-sees-the-future/ch2')
FLOW_DIR = BASE / 'flow_queue'
FLOW_DIR.mkdir(parents=True, exist_ok=True)

CSV_HEADER = [
    "prompt",
    "description",
    "hashtags",
    "videoModel",
    "videoMode",
    "videoDurationSeconds",
    "flowQuantity",
    "videoVoiceReference",
    "flowAspectRatio",
]

HASHTAGS = "#manhwa #2danime #webtoon #investorWhoSeesTheFuture #koreanAnime #shortDrama"
MODEL = "Omni Flash"
MODE = "ingredients"
ASPECT = "9:16"
DELIMITER = "\n\n@@@NEXT@@@\n\n"

MANHUA_STYLE = (
    "Art style: authentic 2D Korean webtoon manhwa anime animation. Crisp clean dark ink line art, "
    "vibrant flat cel-shaded coloring, authentic manhwa character features, fluid 2D anime animation aesthetic. "
    "STRICTLY NOT 3D render, NOT live-action CGI, NOT photorealistic, NOT western comic book style. "
    "Full-bleed 9:16 vertical video. Smooth continuous animation across the 10-second sequence. "
    "Strictly NO comic panels, NO border frames, NO split screen, NO multi-panel collage, "
    "NO on-screen subtitles, NO speech bubbles, NO watermark."
)

# Load the canonical storyboard
sb_path = BASE / 'storyboard_9_16.json'
story = json.loads(sb_path.read_text(encoding='utf-8'))
blocks = story['blocks']

# Cast mapping per block
BLOCK_CAST = [
    ["@Kang Jin-Hoo", "@Drill Sergeant"],
    ["@Kang Jin-Hoo", "@Squadmate"],
    ["@Kang Jin-Hoo", "@Oh Taek-Gyu"],
    ["@Kang Jin-Hoo", "@Oh Taek-Gyu"],
    ["@Kang Jin-Hoo", "@Oh Taek-Gyu"],
    ["@Kang Jin-Hoo", "@Wealthy VIP Customer", "@Store Manager", "@Jin-Hoo's Mother"]
]

def format_frame_prompt(block_idx: int, beat_idx: int, beat: dict, cast_mentions: list) -> str:
    cast_str = " ".join(cast_mentions)
    return f"""{cast_str}
{MANHUA_STYLE}

[Shot Title]: {beat['scene_title']} ({beat['timestamp']})
[Subject & Visual Action]: {beat['action']}
[Camera Kinematics]: {beat['camera']}
[Lighting & Atmosphere]: {beat['sfx']}
[Voiceover Script]: {beat['vo']}
[Sound Effects]: {beat['sfx']}
""".strip()

def format_continuous_prompt(block_idx: int, block: dict, cast_mentions: list) -> str:
    cast_str = " ".join(cast_mentions)
    beats = block['beats']
    title = block['block_title']
    
    lines = [
        cast_str,
        MANHUA_STYLE,
        "",
        f"[Scene Concept]: Single continuous 10-second 2D manhwa animation sequence for Block {block_idx} — {title}.",
        "One continuous camera movement through the environment. Smooth cinematic camera tracking, no comic borders, no split screen, no multi-panel grids.",
        "",
        f"[Sequence Progression across 10 Seconds]:"
    ]
    for b in beats:
        lines.append(f"{b['timestamp']} — {b['label']}: {b['action']} · CAMERA: {b['camera']} · VO: {b['vo']} · SFX: {b['sfx']}")
        lines.append("")
        
    last_beat = beats[-1]
    lines.append(f"[Climax & Hold]: Sequence culminates at 8s-10s with: {last_beat['action']}")
    lines.append(f"[Final Dialogue]: {last_beat['vo']}")
    lines.append("END ON COMPLETE FREEZE FRAME: Subject locks into final pose, motionless through 10s.")
    return "\n".join(lines).strip()

def format_multiline_prompt_txt(block_idx: int, block: dict, cast_mentions: list) -> str:
    cast_str = " ".join(cast_mentions)
    beats = block['beats']
    title = block['block_title']
    
    header = f"VIDEO: E02 B{block_idx} — {title}"
    inputs = f"INPUTS: 9:16 Vertical Video · 10 Seconds · 2D Manhwa Cel Animation · Freeze Frame at 10s"
    
    lines = [cast_str, MANHUA_STYLE, "", header, inputs, ""]
    for b in beats:
        lines.append(f"{b['timestamp']} — {b['label']}: {b['action']} · CAMERA: {b['camera']} · LIGHTING: {b['sfx']} · VO: {b['vo']} · SFX: {b['sfx']}")
        lines.append("")
    return "\n".join(lines).strip()

def build_char_refs_csv(out_path: Path):
    chars = [
        (
            "CHARACTER: KANG JIN-HOO (investor_who_sees_the_future)",
            "KANG JIN-HOO, 23-year-old Korean male, lead protagonist. Recently discharged military veteran, lean athletic build, fair complexion, short textured tousled jet-black hair with natural fringe, sharp intelligent hooded dark eyes, defined jawline, restrained understated calm expression. WARDROBE: cream long-sleeve crewneck pullover sweater, dark indigo slim jeans, clean white low-top sneakers. Full body three-quarter standing studio portrait, clean neutral gray background, cinematic 85mm portrait lighting, ultra-realistic digital webtoon manhwa aesthetics, masterwork fine art fidelity.",
        ),
        (
            "CHARACTER: OH TAEK-GYU (investor_who_sees_the_future)",
            "OH TAEK-GYU, 23-year-old Korean male, co-investor and best friend. Stocky slightly chubby build, round friendly face, short neat dark hair, thick black rectangular eyeglasses, expressive animated eyebrows, warm energetic comedic personality. WARDROBE: heather-gray zip-up hoodie over plain white crewneck t-shirt, dark charcoal casual trousers, comfortable sneakers. Full body three-quarter standing studio portrait, neutral studio background, 85mm soft studio key lighting, premium digital manhwa aesthetics.",
        ),
        (
            "CHARACTER: DRILL SERGEANT & SQUAD (investor_who_sees_the_future)",
            "DRILL SERGEANT, veteran South Korean military artillery instructor in late 20s, rugged weathered face, stern commanding scowl, square jaw, intense dark eyes. WARDROBE: ROK Army digital camouflage combat uniform, tactical Kevlar helmet, chest-rig ammo webbing, combat boots. Standing rigid parade rest, outdoor dusty military training ground background, harsh high-noon tactical sunlight, authentic 2D manhwa line art.",
        ),
        (
            "CHARACTER: JIN-HOO'S MOTHER (investor_who_sees_the_future)",
            "JIN-HOO'S MOTHER, Korean woman in late 50s, petite frail build, weathered gentle face etched with years of sacrifice and manual labor, streaks of gray hair pulled into a modest low bun, warm mournful dark eyes filled with tears. WARDROBE: faded blue janitorial custodial smock over dark work trousers, rubber utility gloves, well-worn waterproof shoes. Kneeling posture, high-end department store marble floor background, dramatic high-contrast spotlight, poignant emotional 2D manhwa drama illustration.",
        ),
        (
            "CHARACTER: WEALTHY VIP CUSTOMER (investor_who_sees_the_future)",
            "WEALTHY VIP CUSTOMER, Korean woman in mid 40s, haughty arrogant sneer, heavily made-up face, sculpted cheekbones, cold contemptuous eyes. WARDROBE: lavish designer beige cashmere overcoat, silk scarf, oversized diamond ring and layered gold necklace, carrying a luxury leather handbag, pristine imported Italian designer leather shoes. Dramatic three-quarter stance, luxury boutique atrium background, dazzling chandeliers, authentic 2D manhwa art.",
        ),
        (
            "CHARACTER: STORE MANAGER (investor_who_sees_the_future)",
            "STORE MANAGER, Korean man in mid 30s, nervous anxious demeanor, sweat beads on forehead, receding slicked hair, subservient bowing posture. WARDROBE: tailored slim-fit navy department store manager suit, gold lapel name tag, polished black dress shoes. Bowing ninety degrees, shiny marble floor background, crisp ambient retail lighting, expressive 2D manhwa line art.",
        ),
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["prompt", "scene name"])
        for prompt, scene_name in chars:
            writer.writerow([prompt, scene_name])
    print(f"[OK] Character references CSV: {out_path.name}")

def main():
    all_36_shots_prompts = []
    all_6_continuous_prompts = []
    
    continuous_rows = []
    fbf_rows = []
    
    for b_idx, block in enumerate(blocks, 1):
        cast = BLOCK_CAST[b_idx - 1]
        title = block['block_title']
        
        # 1. Continuous prompt text
        cont_prompt = format_continuous_prompt(b_idx, block, cast)
        all_6_continuous_prompts.append(cont_prompt)
        
        # 2. Multiline prompts.txt
        multi_txt = format_multiline_prompt_txt(b_idx, block, cast)
        (FLOW_DIR / f"block{b_idx}_prompts.txt").write_text(multi_txt, encoding="utf-8")
        (FLOW_DIR / f"block{b_idx}_video_prompt.txt").write_text(cont_prompt, encoding="utf-8")
        
        # Continuous row for e02.csv
        cont_row = {
            "prompt": cont_prompt,
            "description": f"CONTINUOUS 10S E02 B{b_idx} — {title}",
            "hashtags": HASHTAGS,
            "videoModel": MODEL,
            "videoMode": MODE,
            "videoDurationSeconds": "10",
            "flowQuantity": "1",
            "videoVoiceReference": ", ".join(c.replace("@", "") for c in cast),
            "flowAspectRatio": ASPECT,
        }
        continuous_rows.append(cont_row)
        
        # Per-block continuous queue CSV
        with open(FLOW_DIR / f"block{b_idx}_queue.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
            writer.writeheader()
            writer.writerow(cont_row)
            
        # 3. Per-block frames queue CSV (6 shots per block)
        b_frame_rows = []
        for beat_idx, beat in enumerate(block['beats'], 1):
            f_prompt = format_frame_prompt(b_idx, beat_idx, beat, cast)
            all_36_shots_prompts.append(f_prompt)
            
            f_row = {
                "prompt": f_prompt,
                "description": f"SHOT E02 B{b_idx} Beat {beat_idx} — {beat['scene_title']} ({beat['timestamp']})",
                "hashtags": HASHTAGS,
                "videoModel": MODEL,
                "videoMode": MODE,
                "videoDurationSeconds": "5",
                "flowQuantity": "1",
                "videoVoiceReference": ", ".join(c.replace("@", "") for c in cast),
                "flowAspectRatio": ASPECT,
            }
            b_frame_rows.append(f_row)
            fbf_rows.append(f_row)
            
        with open(FLOW_DIR / f"block{b_idx}_frames_queue.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
            writer.writeheader()
            writer.writerows(b_frame_rows)
            
    # 4. Master continuous queue CSVs: e02.csv and flow_continuous_10s_queue.csv
    with open(FLOW_DIR / "e02.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        writer.writerows(continuous_rows)
        
    with open(FLOW_DIR / "flow_continuous_10s_queue.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        writer.writerows(continuous_rows)
        
    # 5. Master frame-by-frame queue CSV (36 shots)
    with open(FLOW_DIR / "flow_frame_by_frame_queue.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        writer.writerows(fbf_rows)
        
    # 6. Delimited multiline text files with @@@NEXT@@@
    (FLOW_DIR / "flow_6_continuous_blocks.txt").write_text(
        DELIMITER.join(all_6_continuous_prompts), encoding="utf-8"
    )
    (FLOW_DIR / "flow_all_36_shots.txt").write_text(
        DELIMITER.join(all_36_shots_prompts), encoding="utf-8"
    )
    
    # 7. Character reference generation CSV
    build_char_refs_csv(FLOW_DIR / "char_refs_investor.csv")
    
    print("\n[SUCCESS] Chapter 2 Flow Automator Max V3 suite complete!")
    all_files = list(FLOW_DIR.glob("*"))
    print(f"Total files in flow_queue: {len(all_files)}")

if __name__ == "__main__":
    main()
