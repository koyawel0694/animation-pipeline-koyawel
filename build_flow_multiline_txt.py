#!/usr/bin/env python3
"""
build_flow_multiline_txt.py — Compile all video prompts into .txt files for Flow Automator Max.

Formats prompts with the '@@@NEXT@@@' delimiter required by the 'Use multi-line prompt' mode:
  Prompt 1
  @@@NEXT@@@
  Prompt 2
  @@@NEXT@@@
  Prompt 3

Outputs:
1. flow_all_36_shots.txt — All 36 shots for the entire Chapter 1
2. block1_prompts.txt .. block6_prompts.txt — 6 shots per block
3. flow_6_continuous_blocks.txt — 6 continuous 10-second scene blocks
"""

import csv
from pathlib import Path

BASE_DIR = Path("/home/john/manga-reviews/output/the-investor-who-sees-the-future/ch1/flow_queue")
FBF_CSV = BASE_DIR / "flow_frame_by_frame_queue.csv"
CONT_CSV = BASE_DIR / "flow_continuous_10s_queue.csv"

DELIMITER = "\n\n@@@NEXT@@@\n\n"

def main():
    if not FBF_CSV.exists():
        print(f"Error: {FBF_CSV} not found.")
        return

    # 1. Read all 36 frame-by-frame prompts
    all_prompts = []
    with open(FBF_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_prompts.append(row["prompt"].strip())

    print(f"Loaded {len(all_prompts)} individual shot prompts.")

    # 2. Write master all-in-one .txt
    all_txt_path = BASE_DIR / "flow_all_36_shots.txt"
    with open(all_txt_path, "w", encoding="utf-8") as f:
        f.write(DELIMITER.join(all_prompts) + "\n")
    print(f"[OK] Master TXT (all 36 shots): {all_txt_path}")

    # 3. Write per-block .txt files (6 shots each)
    for b_idx in range(1, 7):
        start = (b_idx - 1) * 6
        end = start + 6
        block_prompts = all_prompts[start:end]
        block_txt_path = BASE_DIR / f"block{b_idx}_prompts.txt"
        with open(block_txt_path, "w", encoding="utf-8") as f:
            f.write(DELIMITER.join(block_prompts) + "\n")
        print(f"  - Block {b_idx} TXT (6 shots): {block_txt_path.name}")

    # 4. Write continuous 10s blocks .txt
    if CONT_CSV.exists():
        cont_prompts = []
        with open(CONT_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cont_prompts.append(row["prompt"].strip())

        cont_txt_path = BASE_DIR / "flow_6_continuous_blocks.txt"
        with open(cont_txt_path, "w", encoding="utf-8") as f:
            f.write(DELIMITER.join(cont_prompts) + "\n")
        print(f"[OK] Continuous 10s Blocks TXT (6 blocks): {cont_txt_path}")

if __name__ == "__main__":
    main()
