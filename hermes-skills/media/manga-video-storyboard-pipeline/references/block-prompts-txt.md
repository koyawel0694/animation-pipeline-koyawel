# Block Prompts TXT Production Contract

This contract defines Stage 5 of the manga video storyboard pipeline: producing plain-text prompt files (`.txt`) for generative video models (Google Flow, Kling, Runway, Veo).

## 1. Directory Structure & Files
Prompt files are written directly into the root `flow_queue/` and into per-episode packages when multi-part episodes exist:

```text
output/<series-slug>/ch<chapter>/flow_queue/
output/<series-slug>/ch<chapter>/episodes/ep01/flow_queue/
output/<series-slug>/ch<chapter>/episodes/ep02/flow_queue/
```

Files produced in each `flow_queue/`:
- `block1_prompts.txt` ... `block6_prompts.txt`: Shot-by-shot prompts separated by `\n\n@@@NEXT@@@\n\n`.
- `block1_video_prompt.txt` ... `block6_video_prompt.txt`: Continuous 10-second master prompt per block.
- `flow_6_continuous_blocks.txt`: Sequence of all continuous blocks for the episode separated by `@@@NEXT@@@`.
- `flow_all_36_shots.txt`: Flat concatenation of all individual shot prompts across the episode.
- `prompt_txt_manifest.json`: Machine-readable index of prompt files, shot counts, and active style preset.

**NO CSV FILES REQUIRED**: Plain `.txt` files with `@@@NEXT@@@` delimiters are the required format.

## 2. Shot Prompt Format (`block<N>_prompts.txt`)
Each file contains 6 distinct shot prompts (one for each timing beat) separated by `\n\n@@@NEXT@@@\n\n`.

### Prompt Structure (Style Preset Adaptive)
Each shot prompt follows an exact 8-part specification:
1. **Style Anchor**: Sourced from the active preset in `style_presets.json` (e.g. `photorealistic_live_action`, `webtoon_2d`, `studio_ghibli`, `anime_sakuga_2d`).
2. **Motion Anchor**: Believable motion dynamics matching the media mode (live action camera dolly/crane or fluid 2D key poses).
3. **Negative Anchor**: Negative constraints matching the preset (e.g. banning 2D art when in live-action mode; banning 3D CGI when in 2D mode).
4. **Framing & Aspect Ratio**: Full-bleed 9:16 vertical single shot. NO border frames, NO split screen, NO multi-panel collage, NO subtitles, NO speech bubbles, NO watermark.
5. **Character Identity Anchor**: References the canonical character sheets in `character_refs/`.
6. **Scene Context & Timing**: Series title, episode number (if episodic), block number, beat number, and timestamp range (`0s-1.5s`, `1.5s-3s`, etc.).
7. **Action & Camera**: Precise action description, camera angle, and lens movement.
8. **Dialogue / Audio Cue**: Spoken English lines with parenthesized vocal emotion tags: `(emotion, tone) Dialogue text...`.

## 3. Freeze Frame Directive
Beat 6 of every block must end with the mandatory freeze-frame directive:
`Use the final beat as a complete freeze frame; do not add a new action after the final pose.`

## 4. Multi-Part Episodic Prompts (Copy-Paste Ready)
When a chapter has > 25 pages, `build_serye_storyboard.py` segments the chapter into 60-second episodes (`ep01`, `ep02`, etc.):
1. Each episode directory contains a standalone `flow_queue/` with 1-indexed prompts (`block1_prompts.txt` through `block6_prompts.txt`).
2. Users can open `episodes/ep01/flow_queue/` or `ep02/flow_queue/` and copy-paste each block's prompts directly into Google Flow without manual numbering translation or offset math.
