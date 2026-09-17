# Storyboard Sheet Production Contract

This contract defines Stage 3 of the manga video storyboard pipeline: generating director-level 9:16 vertical storyboard sheets as shown in `/home/john/.codex/attachments/7f01f420-362f-4a66-8ac8-f0a7cc48fecc/image-3.png` and `/home/john/.codex/attachments/7f01f420-362f-4a66-8ac8-f0a7cc48fecc/image-4.png`.

## 1. Directory Structure & File Naming
- **Directory**: `output/<series-slug>/ch<chapter>/nano_storyboards/`
- **File Naming Pattern**: `block<NN>_<slug>.png` (padded two-digit index followed by descriptive beat title in snake_case):
  ```text
  block01_the_question.png
  block02_the_richest_man.png
  block03_before_the_fortune.png
  block04_thirteen_billion.png
  block05_warning_tomorrow.png
  block06_future_real.png
  ```
- **Manifest**: `storyboard_assets_manifest.json` in the chapter directory listing all generated sheets with metadata.

## 2. Canvas & Grid Specifications (image-4.png Layout)
Each storyboard sheet functions as a complete 10-second dramatic short-form sequence:
- **Canvas Aspect Ratio**: 9:16 vertical orientation (`768x1376` pixels).
- **Background & Margins**: Solid matte black (`#050505`) with 4px black gutters separating panels and tiers.
- **Top Header**:
  - Two lines of clean, centered sans-serif white capital text over a black banner:
    - Line 1: `SERYE DRAMA BLOCK — <Series Title> —`
    - Line 2: `Block <N> — <Block Subtitle>` (e.g., `Block 1 — The Question That Changes Everything`).
- **5-Row / 8-Shot Grid Structure**:
  ```text
  ┌────────────────────────────────────────────────────────┐
  │  SERYE DRAMA BLOCK — THE INVESTOR WHO SEES THE FUTURE  │
  │     Block 1 — The Question That Changes Everything     │
  ├──────────────────────────┬─────────────────────────────┤
  │   Panel 1 (Landscape)    │    Panel 2 (Landscape)      │
  │   Beat 1: 0s - 1.5s      │    Beat 2: 1.5s - 3s        │
  ├──────────────────────────┴─────────────────────────────┤
  │            Panel 3 (Full-Width Panoramic)              │
  │                  Beat 3: 3s - 4.5s                     │
  ├──────────────────────────┬─────────────────────────────┤
  │   Panel 4 (Landscape)    │    Panel 5 (Landscape)      │
  │   Beat 4: 4.5s - 6s      │    (Reaction / Insert)      │
  ├──────────────────────────┼─────────────────────────────┤
  │   Panel 6 (Landscape)    │    Panel 7 (Landscape)      │
  │   Beat 5: 6s - 8s        │    (Close-up / Dynamic cut) │
  ├──────────────────────────┴─────────────────────────────┤
  │            Panel 8 (Full-Width / Centered)             │
  │         Beat 6: 8s - 10s — END ON FREEZE FRAME         │
  └────────────────────────────────────────────────────────┘
  ```
  - **Row 1 (2 Panels)**: Two equal landscape shots (~16:9 each).
  - **Row 2 (1 Panel)**: Single full-width cinematic widescreen shot (~21:9).
  - **Row 3 (2 Panels)**: Dynamic split action shots or reaction cuts.
  - **Row 4 (2 Panels)**: Extreme close-up, dramatic insert, or opposing speaker cut.
  - **Row 5 (1 Panel)**: Centered or full-width climactic shot held as a freeze frame.
  - **Total Visual Shots**: Exactly 8 panels across the 5 rows.

## 3. Beat Timing & Labels
Every storyboard sheet corresponds to exactly 6 timing beats totaling 10 seconds:
1. Beat 1: `0s - 1.5s` (The Hook / Question)
2. Beat 2: `1.5s - 3s` (The Escalation / Turn)
3. Beat 3: `3s - 4.5s` (The Reaction / Revelation)
4. Beat 4: `4.5s - 6s` (The Complication / Twist)
5. Beat 5: `6s - 8s` (The Climax / Suspense)
6. Beat 6: `8s - 10s` (The Resolution / Cliffhanger — **END ON FREEZE FRAME**)

Underneath or across each panel tier, bold white all-caps labels indicate the dramatic beat and exact timestamp.

## 4. Visual Quality Standards
- **Narrative Diversity**: Never repeat the exact same image or crop across multiple slots in a block. Split rows must contain distinct angles (e.g. over-the-shoulder vs. reaction face).
- **Freeze Frame Rule**: The 6th beat must end on an explicit held pose without initiating a new action.
- **No Watermarks or Scanlation Junk**: Only clean narrative comic art, characters, and environments.
