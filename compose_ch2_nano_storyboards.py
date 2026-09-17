#!/usr/bin/env python3
"""Compose high-quality 9:16 nano storyboard sheets for Chapter 2 from actual clean frame crops."""
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 768, 1376
ROWS = [(2, 210), (1, 210), (2, 210), (2, 210), (1, 240)]
SLOTS = [0, 1, 2, 3, 3, 4, 4, 5]

BASE = Path('/home/john/manga-reviews/output/the-investor-who-sees-the-future/ch2')
CROPS_DIR = BASE / 'clean_frame_crops'
OUT_DIR = BASE / 'nano_storyboards'
OUT_DIR.mkdir(parents=True, exist_ok=True)

def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_') or 'block'

def font(size: int, bold: bool = False):
    name = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(name, size) if Path(name).exists() else ImageFont.load_default()

def load_storyboard():
    p = BASE / 'storyboard_9_16.json'
    return json.loads(p.read_text(encoding='utf-8'))

def get_block_crops(block_num: int):
    # Find the 6 crops for this block
    pattern = f"b{block_num:02d}_beat"
    crops = {}
    for p in CROPS_DIR.glob(f"{pattern}*.png"):
        m = re.search(rf"b{block_num:02d}_beat(\d+)", p.name)
        if m:
            beat_idx = int(m.group(1)) - 1
            crops[beat_idx] = p
    return crops

def make_panel(crop_path: Path, target_w: int, target_h: int, variant: int = 0):
    img = Image.open(crop_path).convert("RGB")
    zoom = 1.0 if variant == 0 else 1.15
    scale = max(target_w / img.width, target_h / img.height) * zoom
    new_w = int(img.width * scale)
    new_h = int(img.height * scale)
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    if variant == 0:
        left = max(0, (new_w - target_w) // 2)
        top = max(0, (new_h - target_h) // 2)
    else:
        # punch-in variant
        left = max(0, min(new_w - target_w, int((new_w - target_w) * 0.7)))
        top = max(0, min(new_h - target_h, int((new_h - target_h) * 0.4)))
        
    return resized.crop((left, top, left + target_w, top + target_h))

def compose_block_sheet(block_idx: int, block: dict, title: str):
    sheet = Image.new("RGB", (W, H), (5, 5, 5))
    draw = ImageDraw.Draw(sheet)
    
    header_h = 78
    draw.rectangle((0, 0, W, header_h), fill="#050505")
    
    header_text = f"SERYE DRAMA BLOCK — {title} — Block {block_idx}: {block['block_title']}"
    # Truncate if too long
    if len(header_text) > 65:
        header_text = f"SERYE DRAMA BLOCK {block_idx} — {block['block_title']}"
    draw.text((W // 2, header_h // 2), header_text, fill="white", font=font(16, True), anchor="mm")
    
    beats = block.get("beats", [])
    crops = get_block_crops(block_idx)
    
    y = header_h
    frame_index = 0
    for cols, row_h in ROWS:
        gap = 4
        cell_w = (W - gap * (cols - 1)) // cols
        pic_h = row_h - 30
        
        for col in range(cols):
            slot_idx = frame_index
            beat_slot = SLOTS[slot_idx]
            frame_index += 1
            
            # Pick crop path
            crop_path = crops.get(beat_slot) or list(crops.values())[0]
            variant = 1 if slot_idx in (4, 6) else 0
            
            panel_img = make_panel(crop_path, cell_w, pic_h, variant=variant)
            x = col * (cell_w + gap)
            sheet.paste(panel_img, (x, y))
            
            # Label banner
            draw.rectangle((x, y + pic_h, x + cell_w, y + row_h), fill="#050505")
            beat_data = beats[beat_slot] if beat_slot < len(beats) else {}
            lbl = beat_data.get("label", f"BEAT {beat_slot + 1}")
            t_stamp = beat_data.get("timestamp", "")
            label_str = f"{t_stamp}: {lbl}"
            if len(label_str) > 35:
                label_str = label_str[:32] + "..."
            draw.text((x + cell_w // 2, y + pic_h + 15), label_str, fill="white", font=font(11, True), anchor="mm")
            
        y += row_h + gap

    slug = slugify(block['block_title'])
    out_file = OUT_DIR / f"block{block_idx:02d}_{slug}.png"
    sheet.save(out_file, "PNG", optimize=True)
    print(f"[OK] Generated nano storyboard: {out_file.name} ({out_file.stat().st_size} bytes)")
    return out_file

def main():
    sb = load_storyboard()
    title = sb.get("title", "The Investor Who Sees The Future")
    blocks = sb.get("blocks", [])
    
    manifest = {
        "chapter_dir": str(BASE),
        "total_blocks": len(blocks),
        "resolution": f"{W}x{H}",
        "blocks": []
    }
    
    for i, b in enumerate(blocks, 1):
        out_f = compose_block_sheet(i, b, title)
        manifest["blocks"].append({
            "block": i,
            "title": b["block_title"],
            "file": str(out_f)
        })
        
    (BASE / "storyboard_assets_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nAll {len(blocks)} nano storyboard sheets successfully generated!")

if __name__ == "__main__":
    main()
