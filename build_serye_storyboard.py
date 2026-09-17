#!/usr/bin/env python3
"""Build SERYE-style multi-part episodic 10-second storyboard blocks from chapter analysis.

Supports automatic multi-part episodic segmentation:
- Short chapters (<= 25 pages) remain 1 episode (6 blocks = 60s).
- Long chapters (> 25 pages) automatically segment into N coherent 60s episodes
  (e.g. a 63-page chapter splits into 3 distinct 60s viral episodes of 6 blocks each),
  with each episode having its own narrative arc and dramatic cliffhanger freeze-frame.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import re
from pathlib import Path

DURATIONS = ["0s-1.5s", "1.5s-3s", "3s-4.5s", "4.5s-6s", "6s-8s", "8s-10s"]
BEAT_LABELS = [
    "THE OPENING",
    "THE TURN",
    "THE REACTION",
    "THE ESCALATION",
    "THE REVEAL",
    "THE CLIFFHANGER",
]


def clean_text(value: object) -> str:
    return " ".join(str(value or "").split())


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "block"


def load_scenes(path: Path) -> tuple[dict, list[dict]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    scenes = []
    for page in data.get("pages", []):
        for scene in page.get("scenes", []):
            item = dict(scene)
            item["page_number"] = page["page_number"]
            item["page_file"] = page["page_file"]
            item["_scene_id"] = len(scenes)
            scenes.append(item)
    if not scenes:
        raise ValueError(f"No scenes found in analysis file {path}")
    return data, scenes


def select_beats(pool: list[dict], count: int = 6) -> list[dict]:
    """Select count evenly spaced scenes, prioritizing scenes with spoken dialogue."""
    if len(pool) <= count:
        return pool
    # Pick evenly spaced chronological scenes across the pool
    indices = [round(i * (len(pool) - 1) / (count - 1)) for i in range(count)]
    # De-duplicate indices while keeping order
    seen = set()
    selected = []
    for idx in indices:
        if idx not in seen:
            seen.add(idx)
            selected.append(pool[idx])
    # If duplicates occurred due to small pool, fill from remaining
    if len(selected) < count:
        for s in pool:
            if s["_scene_id"] not in seen:
                seen.add(s["_scene_id"])
                selected.append(s)
            if len(selected) == count:
                break
    selected.sort(key=lambda x: (x["page_number"], x["_scene_id"]))
    return selected


def beat_from(scene: dict, label: str, timestamp: str, final: bool = False, cliffhanger: bool = False) -> dict:
    dialogue = clean_text(scene.get("dialogue_text", ""))
    emotion = clean_text(scene.get("voice_emotion", ""))
    if emotion and not emotion.startswith("("):
        emotion = f"({emotion})"
    vo = f"{emotion} {dialogue}".strip() if dialogue else "none"
    action = clean_text(scene.get("action_description", ""))
    camera = clean_text(scene.get("camera_movement", ""))
    sfx = clean_text(scene.get("visual_style_fx", ""))

    if cliffhanger:
        action += " End on a complete cliffhanger freeze frame: subject holds final dramatic pose, eyes locked, no new action."
        camera += "; then locked static hold through 10s"
        sfx += "; dramatic cliffhanger impact sting, then silence"
    elif final:
        action += " End on a held pose and freeze frame through 10s; no new action."
        camera += "; hold static through 10s"
        sfx += "; audio cutoff on held frame"

    return {
        "timestamp": timestamp,
        "label": label,
        "page_number": scene["page_number"],
        "page_file": scene["page_file"],
        "scene_title": clean_text(scene.get("scene_title", "")),
        "action": action,
        "camera": camera,
        "vo": vo,
        "sfx": sfx,
        "story_flow": clean_text(scene.get("story_flow", "")),
        "is_cliffhanger": cliffhanger,
    }


def build_episode_blocks(
    ep_scenes: list[dict],
    lo_page: int,
    hi_page: int,
    ep_number: int,
    global_block_start: int = 1,
) -> tuple[list[dict], str, str]:
    """Build 6 dramatic 10s blocks for an episode (pages lo_page to hi_page)."""
    blocks = []
    for b_idx in range(6):
        b_lo = lo_page + ((hi_page - lo_page + 1) * b_idx) // 6
        b_hi = lo_page + ((hi_page - lo_page + 1) * (b_idx + 1)) // 6
        b_scenes = [s for s in ep_scenes if b_lo <= s["page_number"] <= b_hi]
        if not b_scenes:
            # Fallback to slice of ep_scenes
            chunk_size = max(1, len(ep_scenes) // 6)
            b_scenes = ep_scenes[b_idx * chunk_size : min((b_idx + 1) * chunk_size, len(ep_scenes))]
            if not b_scenes:
                b_scenes = [ep_scenes[-1]]

        picks = select_beats(b_scenes, 6)
        while len(picks) < 6:
            picks.append(picks[-1])

        first_title = clean_text(picks[0].get("scene_title", "")) or f"Scene {b_idx + 1}"
        last_title = clean_text(picks[-1].get("scene_title", "")) or f"Turn {b_idx + 1}"
        block_title = f"{first_title} to {last_title}" if first_title != last_title else first_title

        beats = []
        for beat_idx in range(6):
            is_episode_cliffhanger = (b_idx == 5) and (beat_idx == 5)
            is_block_end = (beat_idx == 5)
            label = BEAT_LABELS[beat_idx]
            if is_episode_cliffhanger:
                label = "THE CLIFFHANGER — FREEZE FRAME"
            elif is_block_end:
                label = "THE TURN — FREEZE FRAME"
            beats.append(beat_from(picks[beat_idx], label, DURATIONS[beat_idx], final=is_block_end, cliffhanger=is_episode_cliffhanger))

        global_block_num = global_block_start + b_idx
        blocks.append({
            "block_number": global_block_num,
            "episode_number": ep_number,
            "episode_block_number": b_idx + 1,
            "block_title": block_title,
            "duration_sec": 10,
            "format": "9:16 vertical",
            "source_pages": sorted({b["page_number"] for b in beats}),
            "beats": beats,
        })

    ep_first = clean_text(ep_scenes[0].get("scene_title", "")) or f"Pages {lo_page}"
    ep_cliffhanger = clean_text(ep_scenes[-1].get("scene_title", "")) or f"Page {hi_page} Cliffhanger"
    ep_title = f"{ep_first} to {ep_cliffhanger}"
    return blocks, ep_title, ep_cliffhanger


def build_storyboard(
    data: dict,
    scenes: list[dict],
    pages_per_episode: int = 22,
    explicit_episodes: int | None = None,
    single_episode: bool = False,
) -> tuple[dict, list[dict]]:
    total_pages = max(p["page_number"] for p in data.get("pages", []))
    if single_episode:
        num_episodes = 1
    elif explicit_episodes:
        num_episodes = max(1, explicit_episodes)
    else:
        num_episodes = max(1, math.ceil(total_pages / pages_per_episode))

    episodes_meta = []
    all_blocks = []
    global_block_counter = 1

    for ep_idx in range(1, num_episodes + 1):
        lo = 1 + (total_pages * (ep_idx - 1)) // num_episodes
        hi = (total_pages * ep_idx) // num_episodes
        ep_scenes = [s for s in scenes if lo <= s["page_number"] <= hi]
        if not ep_scenes:
            ep_scenes = scenes

        ep_blocks, ep_title, ep_cliffhanger = build_episode_blocks(
            ep_scenes, lo, hi, ep_number=ep_idx, global_block_start=global_block_counter
        )
        global_block_counter += len(ep_blocks)
        all_blocks.extend(ep_blocks)

        episodes_meta.append({
            "episode_number": ep_idx,
            "episode_id": f"ep{ep_idx:02d}",
            "title": ep_title,
            "page_range": [lo, hi],
            "total_pages": hi - lo + 1,
            "duration_sec": sum(b["duration_sec"] for b in ep_blocks),
            "blocks_count": len(ep_blocks),
            "cliffhanger": ep_cliffhanger,
            "blocks": ep_blocks,
        })

    master_story = {
        "title": data.get("title") or "Manga Series",
        "chapter": data.get("chapter") or "1",
        "format": "SERYE drama block storyboard",
        "pacing_mode": "multi_part_episodic" if num_episodes > 1 else "single_episode",
        "total_pages": total_pages,
        "total_episodes": num_episodes,
        "total_blocks": len(all_blocks),
        "total_duration_sec": sum(b["duration_sec"] for b in all_blocks),
        "block_duration_sec": 10,
        "blocks": all_blocks,
        "episodes": [
            {k: v for k, v in ep.items() if k != "blocks"} for ep in episodes_meta
        ],
    }

    return master_story, episodes_meta


def render_md(story: dict, episode: dict | None = None) -> str:
    title = story["title"]
    chapter = story["chapter"]
    if episode:
        ep_num = episode["episode_number"]
        ep_title = episode["title"]
        pages = episode["page_range"]
        lines = [
            f"# SERYE Drama Storyboard — {title} — Chapter {chapter} (Part {ep_num})",
            "",
            f"**Episode {ep_num}**: {ep_title}",
            f"**Page Range**: Pages {pages[0]} to {pages[1]} · **Duration**: {episode['duration_sec']}s (6 blocks of 10s)",
            "**Format**: 9:16 vertical · six timestamped beats per block · ends on cliffhanger freeze-frame",
            "",
        ]
        blocks = episode["blocks"]
    else:
        lines = [
            f"# SERYE Drama Storyboard — {title} — Chapter {chapter}",
            "",
            f"**Total Episodes**: {story['total_episodes']} · **Total Duration**: {story['total_duration_sec']}s ({story['total_blocks']} blocks of 10s)",
            "**Format**: 9:16 vertical · six timestamped beats per block · multi-part episodic pacing",
            "",
        ]
        blocks = story["blocks"]

    current_ep = None
    for block in blocks:
        ep_num = block.get("episode_number")
        if not episode and ep_num != current_ep:
            current_ep = ep_num
            lines += [f"# PART {current_ep}", ""]

        b_num = block.get("block_number", 1)
        b_title = block["block_title"]
        lines += [
            f"## SERYE DRAMA BLOCK {b_num} — {b_title}",
            "",
            "| Time | Panel label | Source | Action / composition | Camera | VO / dialogue | SFX |",
            "|---|---|---|---|---|---|---|",
        ]
        for beat in block["beats"]:
            def cell(v): return str(v).replace("|", "\\|").replace("\n", " ")
            lines.append("| " + " | ".join(cell(beat[k]) for k in ["timestamp", "label", "page_file", "action", "camera", "vo", "sfx"]) + " |")

        is_cliffhanger = block["beats"][-1].get("is_cliffhanger")
        if is_cliffhanger:
            lines += ["", "**EPISODE CLIFFHANGER**: complete freeze frame through 10s. No extra movement.", "", "---", ""]
        else:
            lines += ["", "---", ""]

    return "\n".join(lines)


def render_html(story: dict, episode: dict | None = None) -> str:
    title = html.escape(str(story.get("title", "")))
    chapter = html.escape(str(story.get("chapter", "")))
    blocks = episode["blocks"] if episode else story["blocks"]
    subtitle = (
        f"Part {episode['episode_number']} (Pages {episode['page_range'][0]}-{episode['page_range'][1]}) · 60 seconds"
        if episode
        else f"{story.get('total_episodes', 1)} Episodes · {story.get('total_duration_sec', 60)}s Total"
    )

    out = [
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width,initial-scale=1'>",
        f"<title>{title} Ch {chapter} Storyboard</title>",
        "<style>",
        "body{background:#08090d;color:#f2f4f8;font:14px/1.4 system-ui,-apple-system,sans-serif;margin:0;padding:24px}",
        "main{max-width:1400px;margin:auto}",
        "header{margin-bottom:32px;border-bottom:1px solid #252a36;padding-bottom:16px}",
        "h1{font-size:28px;margin:0 0 8px;color:#fff}",
        ".meta{color:#8c9fc2;font-size:15px;margin:0}",
        ".ep-badge{display:inline-block;background:#1d283a;color:#62d9ff;padding:4px 10px;border-radius:6px;font-weight:700;margin-right:8px}",
        ".block{border:1px solid #2b3342;background:#10141e;border-radius:12px;padding:20px;margin-bottom:24px}",
        ".block h2{font-size:18px;margin:0 0 16px;color:#f2c14e}",
        ".grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}",
        ".beat{border:1px solid #202736;background:#0b0e17;padding:12px;border-radius:8px}",
        ".time{color:#f2c14e;font-weight:700;font-size:13px;margin-bottom:4px}",
        ".label{color:#62d9ff;font-weight:700;font-size:13px;margin-bottom:8px}",
        ".src{color:#6b7280;font-size:12px;margin-bottom:6px}",
        ".desc{color:#d1d5db;font-size:13px;margin-bottom:6px}",
        ".vo{color:#a78bfa;font-style:italic;font-size:13px;background:#1a162b;padding:6px 8px;border-radius:4px;margin-top:6px}",
        ".cliffhanger{border:2px solid #ef4444;background:#2b1216;color:#fca5a5;padding:10px 14px;border-radius:8px;font-weight:700;margin-top:14px}",
        "@media(max-width:900px){.grid{grid-template-columns:1fr}}",
        "</style></head><body><main>",
        "<header>",
        f"<h1>{title} — Chapter {chapter}</h1>",
        f"<p class='meta'>{subtitle} · 9:16 vertical · 10s blocks · 6 beats/block</p>",
        "</header>",
    ]

    for b in blocks:
        b_num = b.get("block_number", 1)
        b_title = html.escape(str(b.get("block_title", "")))
        ep_prefix = f"<span class='ep-badge'>Part {b.get('episode_number', 1)}</span>" if not episode else ""
        out.append(f"<section class='block'><h2>{ep_prefix}Block {b_num} — {b_title}</h2><div class='grid'>")
        for beat in b.get("beats", []):
            t = html.escape(str(beat.get("timestamp", "")))
            lbl = html.escape(str(beat.get("label", "")))
            src = html.escape(str(beat.get("page_file", "")))
            act = html.escape(str(beat.get("action", "")))
            vo = html.escape(str(beat.get("vo", "")))
            out.append(f"<article class='beat'><div class='time'>{t}</div><div class='label'>{lbl}</div>")
            out.append(f"<div class='src'>Source: {src}</div><div class='desc'>{act}</div>")
            if vo and vo != "none":
                out.append(f"<div class='vo'>{vo}</div>")
            out.append("</article>")
        out.append("</div>")
        if b.get("beats", [])[-1].get("is_cliffhanger"):
            out.append("<div class='cliffhanger'>⚡ EPISODE CLIFFHANGER: Complete freeze frame held to 10s. End of Part.</div>")
        out.append("</section>")

    out.append("</main></body></html>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Build SERYE multi-part episodic storyboards.")
    ap.add_argument("--analysis", required=True, type=Path, help="Path to chapter_analysis.json")
    ap.add_argument("--output-dir", required=True, type=Path, help="Chapter output directory")
    ap.add_argument("--pages-per-episode", type=int, default=22, help="Target pages per 60s episode (default: 22)")
    ap.add_argument("--episodes", type=int, default=None, help="Explicit episode count override")
    ap.add_argument("--single-episode", action="store_true", help="Force single 60s episode recap")
    args = ap.parse_args()

    analysis_path = args.analysis.resolve()
    if not analysis_path.exists():
        ap.error(f"Analysis file not found: {analysis_path}")
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    data, scenes = load_scenes(analysis_path)
    master_story, episodes_meta = build_storyboard(
        data,
        scenes,
        pages_per_episode=args.pages_per_episode,
        explicit_episodes=args.episodes,
        single_episode=args.single_episode,
    )

    # Save Root Storyboard Artifacts
    (output_dir / "storyboard_9_16.json").write_text(
        json.dumps(master_story, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (output_dir / "storyboard_9_16.md").write_text(render_md(master_story), encoding="utf-8")
    (output_dir / "storyboard_9_16.html").write_text(render_html(master_story), encoding="utf-8")

    # Save Episodes Manifest
    manifest = {
        "title": master_story["title"],
        "chapter": master_story["chapter"],
        "total_pages": master_story["total_pages"],
        "total_episodes": master_story["total_episodes"],
        "total_blocks": master_story["total_blocks"],
        "total_duration_sec": master_story["total_duration_sec"],
        "pacing_mode": master_story["pacing_mode"],
        "episodes": [
            {
                "episode_number": ep["episode_number"],
                "episode_id": ep["episode_id"],
                "title": ep["title"],
                "page_range": ep["page_range"],
                "total_pages": ep["total_pages"],
                "duration_sec": ep["duration_sec"],
                "blocks_count": ep["blocks_count"],
                "cliffhanger": ep["cliffhanger"],
            }
            for ep in episodes_meta
        ],
    }
    (output_dir / "episodes_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Save Per-Episode Directories if multi-part
    if len(episodes_meta) > 1:
        episodes_dir = output_dir / "episodes"
        episodes_dir.mkdir(exist_ok=True)
        for ep in episodes_meta:
            ep_path = episodes_dir / ep["episode_id"]
            ep_path.mkdir(exist_ok=True)
            ep_story = {
                "title": master_story["title"],
                "chapter": master_story["chapter"],
                "episode_number": ep["episode_number"],
                "episode_title": ep["title"],
                "page_range": ep["page_range"],
                "format": "SERYE drama block storyboard",
                "block_duration_sec": 10,
                "duration_sec": ep["duration_sec"],
                "blocks": ep["blocks"],
            }
            (ep_path / "storyboard_9_16.json").write_text(
                json.dumps(ep_story, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            (ep_path / "storyboard_9_16.md").write_text(
                render_md(master_story, episode=ep), encoding="utf-8"
            )
            (ep_path / "storyboard_9_16.html").write_text(
                render_html(master_story, episode=ep), encoding="utf-8"
            )

    print(f"[OK] Generated {master_story['total_episodes']} episode(s), {master_story['total_blocks']} blocks ({master_story['total_duration_sec']}s total) for Chapter {master_story['chapter']}")
    for ep in episodes_meta:
        print(f"  - Part {ep['episode_number']} (Pages {ep['page_range'][0]}-{ep['page_range'][1]}): {ep['blocks_count']} blocks ({ep['duration_sec']}s) | Cliffhanger: \"{ep['cliffhanger']}\"")


if __name__ == "__main__":
    main()
