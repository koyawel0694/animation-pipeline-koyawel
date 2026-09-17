#!/usr/bin/env python3
"""Build SERYE-style 10-second storyboard blocks from canonical chapter analysis."""
import argparse
import html
import json
from pathlib import Path

DURATIONS = ["0s-1.5s", "1.5s-3s", "3s-4.5s", "4.5s-6s", "6s-8s", "8s-10s"]

BLOCKS = [
    {
        "title": "The Question That Changes Everything",
        "pages": (1, 2),
        "labels": ["THE QUESTION", "THE ANSWERS", "THE DREAM", "THE MILLION-WON REALITY", "THE FINAL QUESTION", "THE HOOK"],
        "titles": [
            "Street Interview Opening", "The Hundred Million Won Question", "The Slothful Dream",
            "The Ultimate Hypothetical Question", "The Final Question", "The Realistic Inquiry"
        ],
    },
    {
        "title": "The Man Who Became Richest",
        "pages": (3, 5),
        "labels": ["THE INTERVIEW", "THE RUMOR", "THE DENIAL", "THE GOLDEN EYE", "THE APPARITION", "THE SECRET"],
        "titles": [
            "Interview with the World's Richest Person", "Rumors of Clairvoyance", "Casual Denial",
            "Sudden Activation of the Golden Eye", "Apparition in the Studio", "Golden Gaze and Smirk"
        ],
    },
    {
        "title": "Before the Fortune",
        "pages": (6, 10),
        "labels": ["THE DREAM", "THE DISCHARGE", "THE BASEMENT", "THE OLD LIFE", "THE FRIEND", "THE KEY"],
        "titles": [
            "Waking Up Groggy", "The Discharge Cap", "The Semi-Basement Apartment",
            "Remnants of Family Prosperity", "Introducing Oh Taek-Gyu", "The Bantcoin Encryption Key"
        ],
    },
    {
        "title": "Thirteen Point Five Billion Won",
        "pages": (10, 14),
        "labels": ["THE PRICE", "THE CLARIFICATION", "THE CALCULATION", "THE BOMBSHELL", "THE REQUEST", "THE MEMORY"],
        "titles": [
            "The Price Quote", "The Unit Clarification", "The Staggering Reality",
            "13.5 Billion Won", "Shameless Request", "The Spark of Memory"
        ],
    },
    {
        "title": "The Warning From Tomorrow",
        "pages": (15, 18),
        "labels": ["THE EAGLE", "THE VISION", "THE FIRE", "THE EXCHANGE", "BANKRUPTCY", "SELL EVERYTHING"],
        "titles": [
            "Aura of the Flaming Eagle", "Recurrence of the Vision", "Fiery Inscription",
            "Inquiring About Mountainhill", "The Fiery Warning", "Sell All Your Bantcoin"
        ],
    },
    {
        "title": "The Future Is Real",
        "pages": (19, 23),
        "labels": ["THE SALE", "THE SERVER", "THE EMPTY ACCOUNTS", "THE PANIC", "THE REVELATION", "FREEZE FRAME"],
        "titles": [
            "Taek-Gyu Agrees to Liquidate", "Server Down", "The Empty Accounts Revelation",
            "Community Panic and Uproar", "The Revelation", "Website Promotional End Card"
        ],
    },
]


def load_scenes(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    scenes = []
    for page in data["pages"]:
        for scene in page["scenes"]:
            item = dict(scene)
            item["page_number"] = page["page_number"]
            item["page_file"] = page["page_file"]
            item["_scene_id"] = len(scenes)
            scenes.append(item)
    return data, scenes


def pick_scene(scenes, title, pages, used):
    exact = [s for s in scenes if s.get("scene_title") == title and s["_scene_id"] not in used]
    if exact:
        return exact[0]
    partial = [s for s in scenes if title.lower() in s.get("scene_title", "").lower() and s["_scene_id"] not in used]
    if partial:
        return partial[0]
    in_range = [s for s in scenes if pages[0] <= s["page_number"] <= pages[1] and s["_scene_id"] not in used]
    if in_range:
        return in_range[0]
    any_scene = [s for s in scenes if pages[0] <= s["page_number"] <= pages[1]]
    return any_scene[0] if any_scene else scenes[-1]


def beat_from(scene, label, timestamp, final=False):
    dialogue = scene.get("dialogue_text", "").strip()
    emotion = scene.get("voice_emotion", "").strip()
    vo = f"{emotion} {dialogue}".strip() if dialogue else "none"
    action = scene.get("action_description", "")
    camera = scene.get("camera_movement", "")
    sfx = scene.get("visual_style_fx", "")
    if final:
        action += " End on a complete freeze frame: subject holds final pose, eyes and hands still, no new action."
        camera += "; then locked static hold through 10s"
        sfx += "; final impact, then silence"
    return {
        "timestamp": timestamp,
        "label": label,
        "page_number": scene["page_number"],
        "page_file": scene["page_file"],
        "scene_title": scene.get("scene_title", ""),
        "action": action,
        "camera": camera,
        "vo": vo,
        "sfx": sfx,
        "story_flow": scene.get("story_flow", ""),
    }


def build(data, scenes):
    blocks = []
    for block in BLOCKS:
        used = set()
        beats = []
        for i, (label, title) in enumerate(zip(block["labels"], block["titles"])):
            scene = pick_scene(scenes, title, block["pages"], used)
            used.add(scene["_scene_id"])
            beats.append(beat_from(scene, label, DURATIONS[i], final=(i == 5)))
        blocks.append({
            "block_title": block["title"],
            "duration_sec": 10,
            "format": "9:16 vertical",
            "beats": beats,
            "source_pages": sorted({b["page_number"] for b in beats}),
        })
    return {
        "title": data.get("title"),
        "chapter": data.get("chapter"),
        "format": "SERYE drama block storyboard",
        "block_duration_sec": 10,
        "blocks": blocks,
    }


def render_md(story):
    lines = [f"# SERYE Drama Storyboard — {story['title']} — Chapter {story['chapter']}", "", "Format: 9:16 vertical · 10 seconds per block · six timestamped beats per block", ""]
    for n, block in enumerate(story["blocks"], 1):
        lines += [f"## SERYE DRAMA BLOCK {n} — {block['block_title']}", "", "| Time | Panel label | Source | Action / composition | Camera | VO / dialogue | SFX |", "|---|---|---|---|---|---|---|"]
        for beat in block["beats"]:
            def cell(value): return str(value).replace("|", "\\|").replace("\n", " ")
            lines.append("| " + " | ".join(cell(beat[k]) for k in ["timestamp", "label", "page_file", "action", "camera", "vo", "sfx"]) + " |")
        lines += ["", "FINAL BEAT: freeze frame / held pose through 10s. No extra movement.", "", "---", ""]
    return "\n".join(lines)


def render_html(story):
    css = """
    :root{--bg:#08090d;--panel:#131722;--line:#32394a;--text:#f2f4f8;--muted:#aeb8ca;--gold:#f2c14e;--cyan:#62d9ff}
    *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.4 system-ui,sans-serif}main{max-width:1500px;margin:auto;padding:24px}h1{margin:0 0 6px;font-size:clamp(22px,4vw,38px)}h2{margin:0;color:#fff;font-size:22px}.sub{color:var(--muted);margin-bottom:24px}.block{border:1px solid var(--line);border-radius:14px;background:var(--panel);padding:16px;margin:0 0 28px}.blockhead{display:flex;justify-content:space-between;gap:10px;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:14px}.tag{color:var(--gold);font-weight:800;letter-spacing:.08em;text-transform:uppercase}.strip{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.beat{min-width:0;border:1px solid var(--line);background:#0d111a;border-radius:9px;overflow:hidden}.thumb{aspect-ratio:9/11;background:#222 url('images/PLACEHOLDER') center/cover no-repeat;position:relative}.thumb img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:.42}.time{position:absolute;left:7px;top:7px;background:#000d;color:var(--gold);font-weight:800;padding:3px 6px;border-radius:4px}.label{position:absolute;left:7px;right:7px;bottom:7px;background:#000d;color:#fff;font-weight:900;padding:4px 6px;border-radius:4px;letter-spacing:.04em}.content{padding:9px}.content h3{margin:0 0 5px;color:var(--cyan);font-size:14px}.content p{margin:5px 0;color:var(--muted);font-size:12px}.content b{color:#fff}.freeze{border:1px solid var(--gold);color:var(--gold);padding:7px;margin-top:12px;border-radius:6px;font-weight:700}.topnote{padding:12px;border:1px solid var(--line);border-radius:10px;color:var(--muted);margin:16px 0 22px}@media(max-width:850px){.strip{grid-template-columns:repeat(2,1fr)}}@media(max-width:520px){main{padding:12px}.strip{grid-template-columns:1fr}.blockhead{display:block}}
    """
    out = ["<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>SERYE Storyboard</title><style>", css, "</style></head><body><main>"]
    out.append(f"<h1>SERYE DRAMA STORYBOARD — {html.escape(story['title'])} — CHAPTER {html.escape(str(story['chapter']))}</h1>")
    out.append("<div class='sub'>9:16 vertical · 10 seconds per block · six-panel director strips · canonical sequential image analysis</div>")
    out.append("<div class='topnote'><b>Storyboard contract:</b> Each block runs 10 seconds. Each strip shows six timestamped beats. Last beat freezes on final pose. This is a planning artifact, not a Flow image ingredient.</div>")
    for n, block in enumerate(story["blocks"], 1):
        out.append(f"<section class='block'><div class='blockhead'><div><div class='tag'>SERYE DRAMA BLOCK {n}</div><h2>{html.escape(block['block_title'])}</h2></div><div class='tag'>10s · 9:16</div></div><div class='strip'>")
        for beat in block["beats"]:
            src = "images/" + html.escape(beat["page_file"])
            out.append("<article class='beat'>")
            out.append(f"<div class='thumb'><img src='{src}' alt='{html.escape(beat['page_file'])}'><div class='time'>{html.escape(beat['timestamp'])}</div><div class='label'>{html.escape(beat['label'])}</div></div>")
            out.append("<div class='content'>")
            out.append(f"<h3>{html.escape(beat['scene_title'])}</h3>")
            out.append(f"<p><b>Action:</b> {html.escape(beat['action'])}</p>")
            out.append(f"<p><b>Camera:</b> {html.escape(beat['camera'])}</p>")
            out.append(f"<p><b>VO:</b> {html.escape(beat['vo'])}</p>")
            out.append(f"<p><b>SFX:</b> {html.escape(beat['sfx'])}</p>")
            out.append(f"<p><b>Source:</b> {html.escape(beat['page_file'])}</p></div></article>")
        out.append("</div><div class='freeze'>FINAL BEAT: freeze frame / held pose through 10s. No extra movement.</div></section>")
    out.append("</main></body></html>")
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()
    analysis = Path(args.analysis)
    out = Path(args.output_dir)
    data, scenes = load_scenes(analysis)
    story = build(data, scenes)
    out.mkdir(parents=True, exist_ok=True)
    (out / "storyboard_9_16.json").write_text(json.dumps(story, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "storyboard_9_16.md").write_text(render_md(story), encoding="utf-8")
    (out / "storyboard_9_16.html").write_text(render_html(story), encoding="utf-8")
    print(f"Wrote {len(story['blocks'])} blocks, {sum(len(b['beats']) for b in story['blocks'])} beats")

if __name__ == "__main__":
    main()
