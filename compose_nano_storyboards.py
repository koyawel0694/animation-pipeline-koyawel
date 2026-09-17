#!/usr/bin/env python3
"""Generate art-only storyboard frames with agy, then compose exact SERYE sheets."""
import argparse
import html
import json
import subprocess
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('/home/john/manga-reviews/output/the-investor-who-sees-the-future/ch1')
REF_DIR = ROOT / 'character_refs'
FRAME_DIR = ROOT / 'storyboard_frames'
SHEET_DIR = ROOT / 'nano_storyboards_composed'
AGY = '/home/john/.local/bin/agy'
W, H = 768, 1376

# Exact reference structure: 2 + 1 + 2 + 2 + 1 = 8 frames.
LAYOUT = {
    'block01_the_question': {
        'title': 'Block 1 “The Question That Changes Everything”',
        'frames': [
            ('0s-1.5s', 'STREET OPENING', 'wide establishing shot of a modern Korean pedestrian shopping street; a young male TV reporter stands with a blue microphone while a camera operator films him; no readable signs'),
            ('1.5s-3s', 'THE QUESTION', 'medium close-up of the same reporter in charcoal suit, white shirt, black tie, holding blue microphone toward camera, curious energetic expression'),
            ('3s-4.5s', 'THE ANSWER', 'full-width medium shot of a young Korean woman in beige blouse resting chin on hand, thoughtful expression, urban street background'),
            ('4.5s-6s', 'THE HYPOTHETICAL', 'dynamic three-quarter shot of the same reporter gesturing toward an off-camera interviewee, distinct angle from previous reporter shot'),
            ('4.5s-6s', 'THE REACTION', 'close-up reaction of a puzzled young Korean male interviewee in casual shirt, head tilted, urban background'),
            ('6s-8s', 'THE FINAL ASK', 'macro close-up of reporter microphone and confident lower-face smile, different angle from earlier shots'),
            ('6s-8s', 'THE CLEVER ANSWER', 'close-up of Shin Yuri, young Korean woman with long honey-brown waves and beige blouse, smiling directly at camera'),
            ('8s-10s', 'FREEZE ON CURIOSITY', 'full-width final wide shot: reporter and interviewee group in street composition, reporter holds microphone still and looks toward camera, freeze-frame composition'),
        ],
        'refs': ['street_reporter_ref.png', 'shin_yuri_ref.png'],
    },
    'block02_the_richest_man': {
        'title': 'Block 2 “The Man Who Became Richest”',
        'frames': [
            ('0s-1.5s', 'THE INTERVIEW', 'wide modern television studio interview; female interviewer in navy blazer faces young Korean businessman in dark suit'),
            ('1.5s-3s', 'THE RUMOR', 'close-up of poised female interviewer holding cue cards, inquisitive expression, studio windows behind'),
            ('3s-4.5s', 'THE DENIAL', 'close-up of Kang Jin-Hoo in dark suit calmly denying a rumor, controlled smile, studio lighting'),
            ('4.5s-6s', 'THE EYE', 'extreme close-up of Kang Jin-Hoo turning sharply, one amber-gold eye glowing with supernatural perception, no gore'),
            ('4.5s-6s', 'THE SHAMAN', 'separate close-up of ancient Korean shamanic spirit in green and gold ceremonial robes, pale glowing eyes, emerald mist'),
            ('6s-8s', 'THE APPARITION', 'wide studio shot: ordinary camera crew in foreground, supernatural shaman spirit revealed behind them, distinct composition'),
            ('6s-8s', 'THE GAZE', 'close-up of Kang Jin-Hoo staring toward unseen apparition, calm but burdened, golden eye reflection'),
            ('8s-10s', 'FREEZE ON THE SECRET', 'full-width final studio shot, Kang Jin-Hoo seated perfectly still while supernatural glow reflects behind him, freeze frame'),
        ],
        'refs': ['kang_jin_hoo_ref.png', 'female_interviewer_ref.png', 'spirit_shaman_ref.png'],
    },
    'block03_before_the_fortune': {
        'title': 'Block 3 “Before the Fortune”',
        'frames': [
            ('0s-1.5s', 'THE DREAM', 'Kang Jin-Hoo wakes groggy on a floral mattress in a cramped room, morning light'),
            ('1.5s-3s', 'THE BASEMENT', 'wide semi-basement apartment interior, Kang Jin-Hoo alone among modest furniture and recycled newspapers'),
            ('3s-4.5s', 'THE OLD LIFE', 'quiet close-up of Kang Jin-Hoo exhaling, tired expression, family apartment details behind'),
            ('4.5s-6s', 'THE FRIEND', 'Oh Taek-Gyu in gray hoodie and glasses leans forward excitedly in apartment, distinct medium shot'),
            ('4.5s-6s', 'THE COLLECTION', 'different angle: Oh Taek-Gyu gestures toward shelves of gaming collectibles, friendly comedic expression'),
            ('6s-8s', 'THE KEY', 'close-up of Oh Taek-Gyu whispering a secret toward Kang Jin-Hoo, hands visible, no readable screen text'),
            ('6s-8s', 'THE MEMORY', 'Kang Jin-Hoo reaction close-up as he realizes the value of the lost cryptocurrency, shocked eyes'),
            ('8s-10s', 'FREEZE ON THE KEY', 'full-width apartment two-shot, Oh Taek-Gyu holds still mid-reveal and Kang Jin-Hoo looks toward camera, freeze frame'),
        ],
        'refs': ['kang_jin_hoo_ref.png', 'oh_taek_gyu_ref.png'],
    },
    'block04_thirteen_billion': {
        'title': 'Block 4 “Thirteen Point Five Billion Won”',
        'frames': [
            ('0s-1.5s', 'THE PRICE', 'two friends seated on apartment floor, Oh Taek-Gyu casually explains unexpected cryptocurrency value, no screen text'),
            ('1.5s-3s', 'THE UNIT', 'close-up of Oh Taek-Gyu raising one finger to clarify the cryptocurrency unit, distinct pose'),
            ('3s-4.5s', 'THE CALCULATION', 'Kang Jin-Hoo calculates mentally with fingers near chin, sweat drop, apartment light'),
            ('4.5s-6s', 'THE BOMBSHELL', 'Oh Taek-Gyu makes a shrugging gesture, overwhelmed by the fortune, bright window behind'),
            ('4.5s-6s', 'THE EYE', 'extreme close-up of Kang Jin-Hoo eye widening as memory clicks, clean shock lines'),
            ('6s-8s', 'THE REQUEST', 'Kang Jin-Hoo leans urgently toward friend asking for a share, distinct medium two-shot'),
            ('6s-8s', 'THE REFUSAL', 'Oh Taek-Gyu folds arms and refuses with comedic firmness, different camera angle'),
            ('8s-10s', 'FREEZE ON MEMORY', 'full-width final shot: Kang Jin-Hoo suddenly looks toward a remembered vision, hand raised, freeze frame'),
        ],
        'refs': ['kang_jin_hoo_ref.png', 'oh_taek_gyu_ref.png'],
    },
    'block05_warning_tomorrow': {
        'title': 'Block 5 “The Warning From Tomorrow”',
        'frames': [
            ('0s-1.5s', 'THE EAGLE', 'realistic bald eagle perched on ledge surrounded by controlled golden-pink flame aura, no text'),
            ('1.5s-3s', 'THE VISION', 'flaming eagle spreads wings above stunned Kang Jin-Hoo, supernatural golden light'),
            ('3s-4.5s', 'THE EXCHANGE', 'Kang Jin-Hoo turns serious toward Oh Taek-Gyu in apartment, shoulder-over-view'),
            ('4.5s-6s', 'THE NAME', 'Oh Taek-Gyu answers calmly while Kang Jin-Hoo listens, modern apartment, no screens'),
            ('4.5s-6s', 'BANKRUPTCY', 'symbolic vision: dark exchange building losing lights under ominous red warning glow, no readable text, no UI'),
            ('6s-8s', 'THE WARNING', 'Kang Jin-Hoo urgently tells Oh Taek-Gyu to sell, intense face-to-face two-shot'),
            ('6s-8s', 'TRUST ME', 'Oh Taek-Gyu searches Kang Jin-Hoo face, conflicted but listening, distinct close-up'),
            ('8s-10s', 'FREEZE ON DECISION', 'full-width apartment shot: both men hold still beside the table, Kang Jin-Hoo resolute, freeze frame'),
        ],
        'refs': ['kang_jin_hoo_ref.png', 'oh_taek_gyu_ref.png', 'spirit_shaman_ref.png'],
    },
    'block06_future_real': {
        'title': 'Block 6 “The Future Is Real”',
        'frames': [
            ('0s-1.5s', 'THE SALE', 'Oh Taek-Gyu in gray hoodie confirms he will liquidate, apartment two-shot, no screen text'),
            ('1.5s-3s', 'THE SERVER', 'Oh Taek-Gyu reacts to a sudden technical failure, close-up of face only; phone screen is abstract blank shapes, no words'),
            ('3s-4.5s', 'THE ACCOUNTS', 'Kang Jin-Hoo pale and shocked in close-up, purple stress lines, no UI or text'),
            ('4.5s-6s', 'THE PANIC', 'abstract close-up of hands and blank device glow with worried silhouettes behind, no readable text or charts'),
            ('4.5s-6s', 'THE DEMAND', 'Oh Taek-Gyu grabs Kang Jin-Hoo sleeve in panic, modern apartment, distinct action shot'),
            ('6s-8s', 'THE TRUTH', 'Kang Jin-Hoo calms, hand over chest, burdened expression, no extra characters'),
            ('6s-8s', 'THE REVELATION', 'close-up of Kang Jin-Hoo looking directly forward, determined to confess his ability, clean background'),
            ('8s-10s', 'I SEE THE FUTURE — FREEZE FRAME', 'full-width final apartment shot: Kang Jin-Hoo stands perfectly still facing camera, Oh Taek-Gyu frozen behind him in stunned silence, modern setting, no fantasy swordsman, no advertisement, no website, no text except the locally added label'),
        ],
        'refs': ['kang_jin_hoo_ref.png', 'oh_taek_gyu_ref.png'],
    },
}


def load_font(size, bold=False):
    paths = ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    for p in paths:
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def run_agy(prompt, out):
    r = subprocess.run([AGY, '--model', 'gemini-3.8-flash-medium', '--effort', 'medium', '--print-timeout', '15m', '-p', prompt], capture_output=True, text=True, timeout=1000)
    if r.returncode: raise RuntimeError(r.stderr.strip() or f'agy exit {r.returncode}')
    if not out.exists(): raise RuntimeError(f'agy claimed success but output missing: {out}')


def prompt_for_frame(block, index, spec, output):
    refs = '\n'.join(str(REF_DIR / x) for x in block['refs'])
    return f"""Use Nano Banana Pro image generation through Google Antigravity. Generate ONE art-only storyboard frame, not a sheet and not a collage.

Series: The Investor Who Sees The Future. Block: {block['title']}. Shot {index+1} of 8.
SHOT LABEL FOR LOCAL COMPOSITOR ONLY: {spec[1]}
SHOT TIMING FOR LOCAL COMPOSITOR ONLY: {spec[0]}

Visual shot:
{spec[2]}

Read and use these character reference sheets:
{refs}

Requirements:
- Modern premium Korean manhwa/webtoon art, crisp clean linework, realistic anatomy, controlled cell shading.
- 16:9? No. Generate portrait 9:16 art frame, 768x1152 or similar portrait frame.
- Preserve reference faces, hair, wardrobe, body proportions exactly.
- No text, no labels, no timestamp, no speech bubbles, no UI words, no logos, no watermark, no ad, no website, no unrelated characters.
- One clear camera composition. No duplicate panels. No collage. No storyboard sheet.
- For final shot, hold characters in a clear freeze-frame pose.
Save PNG exactly here: {output}
"""


def compose(block_key, block, frames):
    SHEET_DIR.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (W, H), '#050505')
    draw = ImageDraw.Draw(sheet)
    header_h = 78
    draw.rectangle((0,0,W,header_h), fill='#050505')
    header_font = load_font(18, True)
    title = f"SERYE DRAMA BLOCK — The Investor Who Sees The Future — {block['title']}"
    draw.text((W//2, header_h//2), title, fill='white', font=header_font, anchor='mm')
    # Rows: 2,1,2,2,1
    y = header_h
    row_heights = [210, 210, 210, 210, 240]
    groups = [[0,1],[2],[3,4],[5,6],[7]]
    label_font = load_font(13, True)
    for row, (height, indices) in enumerate(zip(row_heights, groups)):
        cols = len(indices)
        gap = 4
        cell_w = (W - gap*(cols-1)) // cols
        for j, idx in enumerate(indices):
            x = j*(cell_w+gap)
            img = Image.open(frames[idx]).convert('RGB')
            # cover cell, preserving frame artwork
            scale = max(cell_w/img.width, (height-28)/img.height)
            img = img.resize((int(img.width*scale), int(img.height*scale)), Image.Resampling.LANCZOS)
            left=(img.width-cell_w)//2; top=(img.height-(height-28))//2
            crop=img.crop((left,top,left+cell_w,top+height-28))
            sheet.paste(crop,(x,y))
            draw.rectangle((x,y+height-28,x+cell_w,y+height),fill='#050505')
            timestamp, label, _ = block['frames'][idx]
            text=f'{timestamp}: {label}'
            draw.text((x+cell_w//2,y+height-14),text,fill='white',font=label_font,anchor='mm')
        y += height + 4
    out=SHEET_DIR/f'{block_key}.png'
    sheet.save(out, optimize=True)
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--block', choices=list(LAYOUT), default=None)
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--compose-only', action='store_true')
    args=ap.parse_args()
    FRAME_DIR.mkdir(parents=True,exist_ok=True); SHEET_DIR.mkdir(parents=True,exist_ok=True)
    keys=[args.block] if args.block else list(LAYOUT)
    for key in keys:
        block=LAYOUT[key]; frames=[]
        for i,spec in enumerate(block['frames']):
            out=FRAME_DIR/f'{key}_{i+1:02d}.png'
            if not args.compose_only or not out.exists():
                print(f'[FRAME] {key} {i+1}/8',flush=True)
                run_agy(prompt_for_frame(block,i,spec,out),out)
            frames.append(out)
        composed=compose(key,block,frames)
        print(f'[COMPOSED] {composed}',flush=True)

if __name__=='__main__': main()
