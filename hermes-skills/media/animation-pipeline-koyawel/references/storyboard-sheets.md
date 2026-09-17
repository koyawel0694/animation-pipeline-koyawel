# Storyboard Production Contract (Narrative Blocks)

This contract defines Stage 4 of the manga video storyboard pipeline: generating structured 10-second SERYE drama storyboard blocks.

## 1. Important Architecture Note
**Visual storyboard PNG sheet compositing (legacy `nano_storyboards/*.png` and `clean_frame_crops/`) is REMOVED from the standard pipeline deliverables.**
Generative video engines (Google Flow, Kling, Runway) consume plain-text shot prompts and character reference sheets—not composite multi-panel collage images.

The primary storyboard deliverables are:
1. `storyboard_9_16.json`: Machine-readable canonical storyboard metadata.
2. `storyboard_9_16.md`: Human-readable director overview table.
3. `storyboard_9_16.html`: Responsive visual director overview.

## 2. Episodic Pacing & Timing Contract
- **Block Duration**: 10 seconds per block.
- **Beats per Block**: Exactly 6 timing beats per block:
  - `0s-1.5s`: THE OPENING (establishing the shot, characters, or situation)
  - `1.5s-3s`: THE TURN (new action, camera shift, or character reaction)
  - `3s-4.5s`: THE REACTION (emotional close-up or counter-movement)
  - `4.5s-6s`: THE ESCALATION (rising conflict, technique invocation, or power reveal)
  - `6s-8s`: THE REVEAL (dramatic impact or climax of the block)
  - `8s-10s`: THE CLIFFHANGER / FREEZE FRAME (ends with an explicit freeze-frame instruction)
- **Freeze-Frame Rule**: Beat 6 must always include: `Use the final beat as a complete freeze frame; do not add a new action after the final pose.`

## 3. Multi-Part Episodic Segmentation for Long Chapters
To avoid narrative cramming:
- **Short Chapters (<= 25 pages)**: Standard single 60s episode (6 blocks = 60s total).
- **Long Chapters (> 25 pages, e.g. 50-70 pages)**: Automatically segmented into coherent 60s episodes (~20-22 pages per episode). Each episode has its own 6-block narrative arc and cliffhanger freeze frame, stored in `episodes/ep01/`, `ep02/`, etc. with a unified `storyboard_9_16.json` and `episodes_manifest.json`.
