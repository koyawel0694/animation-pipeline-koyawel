#!/usr/bin/env python3
"""Generate 36 clean 9:16 frame crops for Chapter 2 from validated panel coordinates."""
from pathlib import Path
from PIL import Image

BASE = Path('/home/john/manga-reviews/output/the-investor-who-sees-the-future/ch2')
CROPS_DIR = BASE / 'clean_frame_crops'
IMAGES_DIR = BASE / 'images'
CROPS_DIR.mkdir(parents=True, exist_ok=True)

BEATS = [
    # Block 1: The Mortar Range Drill
    {"block": 1, "beat": 1, "page": 1, "y": 3600, "title": "mortar_range_flashback"},
    {"block": 1, "beat": 2, "page": 1, "y": 5200, "title": "sergeant_reprimand"},
    {"block": 1, "beat": 3, "page": 1, "y": 6800, "title": "disciplined_salute"},
    {"block": 1, "beat": 4, "page": 1, "y": 9600, "title": "golden_glow_canopy"},
    {"block": 1, "beat": 5, "page": 2, "y": 1200, "title": "golden_eagle_perched"},
    {"block": 1, "beat": 6, "page": 2, "y": 6500, "title": "eagle_streak_overhead"},

    # Block 2: The Premonition and Explosion
    {"block": 2, "beat": 1, "page": 3, "y": 1200, "title": "squadmate_denial"},
    {"block": 2, "beat": 2, "page": 3, "y": 5800, "title": "golden_hud_warning"},
    {"block": 2, "beat": 3, "page": 4, "y": 1200, "title": "loading_mortar_shell"},
    {"block": 2, "beat": 4, "page": 4, "y": 4500, "title": "fatal_countdown_misfire"},
    {"block": 2, "beat": 5, "page": 4, "y": 7200, "title": "desperate_tackle_dive"},
    {"block": 2, "beat": 6, "page": 4, "y": 9600, "title": "catastrophic_detonation"},

    # Block 3: Twice Means A Superpower
    {"block": 3, "beat": 1, "page": 5, "y": 1800, "title": "civilian_studio_reflectio"},
    {"block": 3, "beat": 2, "page": 5, "y": 5800, "title": "miraculous_survival_talk"},
    {"block": 3, "beat": 3, "page": 6, "y": 1200, "title": "twice_is_a_superpower"},
    {"block": 3, "beat": 4, "page": 6, "y": 3600, "title": "jinhoo_skepticism"},
    {"block": 3, "beat": 5, "page": 6, "y": 6200, "title": "otaku_fortitude_smirk"},
    {"block": 3, "beat": 6, "page": 6, "y": 9500, "title": "practical_matters_share"},

    # Block 4: The 1.24 Billion Won Share
    {"block": 4, "beat": 1, "page": 7, "y": 1200, "title": "taekgyu_stunned_silence"},
    {"block": 4, "beat": 2, "page": 7, "y": 3800, "title": "figure_hostage_extortion"},
    {"block": 4, "beat": 3, "page": 7, "y": 6500, "title": "hostage_crisis_panic"},
    {"block": 4, "beat": 4, "page": 8, "y": 1200, "title": "sisters_tax_warning"},
    {"block": 4, "beat": 5, "page": 8, "y": 4200, "title": "della_island_tax_haven"},
    {"block": 4, "beat": 6, "page": 8, "y": 8800, "title": "solemn_partner_pledge"},

    # Block 5: The 500 Million Won Wire
    {"block": 5, "beat": 1, "page": 9, "y": 1200, "title": "first_wire_transfer"},
    {"block": 5, "beat": 2, "page": 9, "y": 7200, "title": "kh_bank_passbook_euphoria"},
    {"block": 5, "beat": 3, "page": 10, "y": 2200, "title": "progressive_gift_tax_plan"},
    {"block": 5, "beat": 4, "page": 10, "y": 7800, "title": "filial_devotion_street"},
    {"block": 5, "beat": 5, "page": 11, "y": 1200, "title": "luxury_department_atrium"},
    {"block": 5, "beat": 6, "page": 11, "y": 3500, "title": "entering_high_end_boutiqu"},

    # Block 6: The Humiliation at the Department Store
    {"block": 6, "beat": 1, "page": 11, "y": 7200, "title": "vip_harsh_commotion"},
    {"block": 6, "beat": 2, "page": 11, "y": 8800, "title": "bystanders_whispering"},
    {"block": 6, "beat": 3, "page": 12, "y": 1500, "title": "verbal_abuse_over_shoes"},
    {"block": 6, "beat": 4, "page": 12, "y": 4800, "title": "manager_forced_kneeling"},
    {"block": 6, "beat": 5, "page": 12, "y": 8800, "title": "jinhoo_mounting_horror"},
    {"block": 6, "beat": 6, "page": 13, "y": 1800, "title": "mother_humiliation_clif"},
]

w_target = 800
h_target = 1422

for b in BEATS:
    page_num = b['page']
    page_path = IMAGES_DIR / f"page_{page_num:03d}.webp"
    im = Image.open(page_path)
    w, h = im.size
    
    y = b['y']
    max_y = max(0, h - h_target)
    y_clamped = max(0, min(y, max_y))
    
    crop = im.crop((0, y_clamped, w_target, y_clamped + h_target))
    slug = b['title'][:25]
    out_name = f"b{b['block']:02d}_beat{b['beat']}_{slug}.png"
    out_path = CROPS_DIR / out_name
    crop.save(out_path, "PNG", optimize=True)

print(f"[OK] Generated {len(list(CROPS_DIR.glob('*.png')))} clean frame crops.")
