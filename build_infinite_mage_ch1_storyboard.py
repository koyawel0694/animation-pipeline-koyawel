#!/usr/bin/env python3
import argparse, json, html, re
from pathlib import Path

TIMES = ["0s-1.5s", "1.5s-3s", "3s-4.5s", "4.5s-6s", "6s-8s", "8s-10s"]

def clean(v):
    return " ".join(str(v or "").split())

def load_scenes(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    scenes=[]
    for page in data.get("pages", []):
        for scene in page.get("scenes", []):
            s=dict(scene); s["page_number"]=page["page_number"]; s["page_file"]=page["page_file"]; scenes.append(s)
    return data, scenes

def slug(v): return re.sub(r"[^a-z0-9]+", "_", v.lower()).strip("_") or "block"

def choose(scenes, lo, hi, i):
    pool=[s for s in scenes if lo <= s["page_number"] <= hi]
    if not pool: pool=scenes
    # six evenly-spaced chronological picks, preferring distinct scenes
    idx=min(len(pool)-1, round(i*(len(pool)-1)/5))
    return pool[idx]

def beat(scene, label, t, final=False):
    action=clean(scene.get("action_description")); camera=clean(scene.get("camera_movement")); sfx=clean(scene.get("visual_style_fx"))
    if final:
        action += " End on a complete freeze frame: hold the final pose with no new action."
        camera = (camera + "; then locked static hold through 10 seconds").strip("; ")
        sfx = (sfx + "; final impact, then silence").strip("; ")
    emotion=clean(scene.get("voice_emotion")); dialogue=clean(scene.get("dialogue_text"))
    vo=(emotion + " " + dialogue).strip() if dialogue else "none"
    return {"timestamp":t,"label":label,"page_number":scene["page_number"],"page_file":scene["page_file"],"scene_title":clean(scene.get("scene_title")),"action":action,"camera":camera,"vo":vo,"sfx":sfx,"story_flow":clean(scene.get("story_flow"))}

def render_md(story):
    lines=[f"# SERYE Drama Storyboard — {story['title']} — Chapter {story['chapter']}","","Format: 9:16 vertical · 10 seconds per block · six timestamped beats per block","", "Source: canonical single sequential page analysis.",""]
    for n,b in enumerate(story["blocks"],1):
        lines += [f"## SERYE DRAMA BLOCK {n} — {b['block_title']}","","| Time | Label | Source | Scene | Action | Camera | English VO | |","|---|---|---|---|---|---|---|---|"]
        for x in b["beats"]:
            vals=[x[k] for k in ["timestamp","label","page_file","scene_title","action","camera","vo"]]
            lines.append("| " + " | ".join(str(v).replace("|","\\|").replace("\n"," ") for v in vals) + " |")
        lines += ["","FINAL BEAT: complete freeze frame through 10 seconds; no new action.","","---",""]
    return "\n".join(lines)

def render_html(story):
    out=["<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>The Infinite Mage Storyboard</title><style>body{background:#08090d;color:#f2f4f8;font:14px/1.4 system-ui;margin:0;padding:24px}main{max-width:1500px;margin:auto}.block{border:1px solid #384052;background:#131722;border-radius:12px;padding:16px;margin:0 0 24px}h1{font-size:30px}h2{font-size:21px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.beat{border:1px solid #384052;background:#0d111a;padding:10px;border-radius:8px}.time,.label{color:#f2c14e;font-weight:800}.label{color:#62d9ff}.freeze{border:1px solid #f2c14e;color:#f2c14e;padding:8px;margin-top:12px}@media(max-width:800px){.grid{grid-template-columns:1fr}}</style></head><body><main>"]
    out.append(f"<h1>SERYE DRAMA STORYBOARD — {html.escape(story['title'])} — CHAPTER {story['chapter']}</h1>")
    out.append("<p>9:16 vertical · 10 seconds per block · canonical single sequential page analysis · English VO cues</p>")
    for n,b in enumerate(story["blocks"],1):
        out.append(f"<section class='block'><h2>BLOCK {n} — {html.escape(b['block_title'])}</h2><div class='grid'>")
        for x in b["beats"]:
            out.append("<article class='beat'>")
            out.append(f"<div class='time'>{html.escape(x['timestamp'])}</div><div class='label'>{html.escape(x['label'])}</div><h3>{html.escape(x['scene_title'])}</h3>")
            for k in ["page_file","action","camera","vo","sfx"]:
                out.append(f"<p><b>{k}:</b> {html.escape(str(x[k]))}</p>")
            out.append("</article>")
        out.append("</div><div class='freeze'>FINAL BEAT: complete freeze frame through 10 seconds; no new action.</div></section>")
    out.append("</main></body></html>")
    return "".join(out)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--analysis",required=True,type=Path); ap.add_argument("--output-dir",required=True,type=Path); args=ap.parse_args()
    data,scenes=load_scenes(args.analysis)
    if not scenes: raise SystemExit("No scenes in analysis")
    # Use six chronological chapter bands; every band contributes six distinct beats.
    total=max(s["page_number"] for s in scenes)
    ranges=[]
    for n in range(6):
        lo=1+(total*n)//6; hi=(total*(n+1))//6
        ranges.append((lo,hi))
    blocks=[]
    for n,(lo,hi) in enumerate(ranges,1):
        picks=[choose(scenes,lo,hi,i) for i in range(6)]
        first=clean(picks[0].get("scene_title")) or f"Pages {lo}-{hi}"
        last=clean(picks[-1].get("scene_title")) or "Chapter turn"
        title=f"{first} to {last}"
        labels=["THE OPENING","THE TURN","THE REACTION","THE ESCALATION","THE REVEAL","THE CLIFFHANGER"]
        blocks.append({"block_title":title,"duration_sec":10,"format":"9:16 vertical","source_pages":sorted({x["page_number"] for x in picks}),"beats":[beat(picks[i],labels[i],TIMES[i],i==5) for i in range(6)]})
    story={"title":"The Infinite Mage","chapter":"1","format":"SERYE drama block storyboard","block_duration_sec":10,"blocks":blocks,"source_analysis":str(args.analysis.resolve())}
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/"storyboard_9_16.json").write_text(json.dumps(story,indent=2,ensure_ascii=False),encoding="utf-8")
    (args.output_dir/"storyboard_9_16.md").write_text(render_md(story),encoding="utf-8")
    (args.output_dir/"storyboard_9_16.html").write_text(render_html(story),encoding="utf-8")
    print(f"[OK] Wrote {len(blocks)} blocks, {sum(len(b['beats']) for b in blocks)} beats from {len(scenes)} analyzed scenes")

if __name__=='__main__': main()
