# Block Prompts TXT Production Contract

This contract defines Stage 4 of the manga video storyboard pipeline: producing plain-text prompt files (`.txt`) for generative video models (Google Flow, Kling, Runway) as shown in `/home/john/.codex/attachments/7f01f420-362f-4a66-8ac8-f0a7cc48fecc/image-5.png`.

## 1. Directory Structure & Files
All prompt files are written directly into:
```text
output/<series-slug>/ch<chapter>/flow_queue/
```

Files produced per chapter:
- `block1_prompts.txt` ... `block6_prompts.txt`: Shot-by-shot prompts separated by `@@@NEXT@@@`.
- `block1_video_prompt.txt` ... `block6_video_prompt.txt`: Continuous 10-second master prompt per block.
- `flow_6_continuous_blocks.txt`: Sequence of all 6 blocks separated by `@@@NEXT@@@`.
- `flow_all_36_shots.txt`: Flat concatenation of all individual shot prompts across all blocks.
- `prompt_txt_manifest.json`: Machine-readable index of prompt files and shot counts.

**NO CSV FILES REQUIRED**: Disregard older Flow Automator CSV queues. Plain `.txt` files with `@@@NEXT@@@` delimiters are the primary format.

## 2. Shot Prompt Format (`block<N>_prompts.txt`)
Each file contains 6 distinct shot prompts (one for each timing beat) separated by `\n\n@@@NEXT@@@\n\n`.

### Prompt Structure
Each shot prompt follows an exact 8-part specification:
```text
Art style: authentic 2D Korean webtoon manhwa anime animation. Crisp clean dark ink line art, vibrant flat cel-shaded coloring, authentic manhwa character features, fluid 2D animation. STRICTLY NOT 3D render, NOT live-action CGI, NOT photorealistic, NOT western comic-book style. Full-bleed 9:16 vertical single shot. NO comic panels, NO border frames, NO split screen, NO multi-panel collage, NO subtitles, NO speech bubbles, NO watermark.
Series: <Series Title>.
Storyboard block <N>, beat <M>, timing <start>s-<end>s.
Create one continuous full-bleed shot for the beat labelled <BEAT_LABEL>.
Action and composition: <Detailed visual description of characters, environment, blocking, and movement>.
Camera movement: <Specific kinematic camera direction, e.g. "Slow crane down from high angle toward reporter">.
English dialogue or voiceover cue: (<emotion, delivery>) <Spoken line in English>.
Sound design suggestion: <Environmental audio, BGM vibe, ambient lighting, color palette>.
Narrative source anchor: <page_file.webp>; preserve the scene, but do not reproduce the source page, gutters, captions, or scanlation text.
```

### Critical Rules
1. **Style Lock Anchor**: Every prompt must begin with the exact 2D Korean webtoon manhwa anime animation block.
2. **Dialogue & VO Emotion**:
   - Voiceover dialogue must be strictly in **English**.
   - Emotion cues must sit **INSIDE parentheses** at the start of the line: e.g. `(energetic, professional broadcast tone)`, `(stunned, disbelieving whisper)`.
   - Never separate emotions into trailing commentary.
3. **Freeze Frame Ending**:
   - The 6th prompt of each block (timing `8s-10s`) must end with an explicit freeze-frame directive:
     ```text
     Use the final beat as a complete freeze frame; do not add a new action after the final pose.
     ```
4. **Delimiter**: Exactly `\n\n@@@NEXT@@@\n\n` between shots.

## 3. Continuous Video Prompt (`block<N>_video_prompt.txt`)
Provides a single unified prompt to animate the entire 10-second block in tools that accept a full scene description rather than separate cuts:
```text
Art style: authentic 2D Korean webtoon manhwa anime animation...
Series: <Series Title>.
Create one coherent 10-second vertical drama block, storyboard block <N>: <Block Title>.
Maintain exact character identity, wardrobe, setting continuity, and chronological action across the beats.
Beat 1 (0s-1.5s): ...
Beat 2 (1.5s-3s): ...
Beat 3 (3s-4.5s): ...
Beat 4 (4.5s-6s): ...
Beat 5 (6s-8s): ...
Beat 6 (8s-10s): ...
Use the final beat as a complete freeze frame; do not add a new action after the final pose.
```
