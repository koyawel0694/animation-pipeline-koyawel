# Chapter Video Production Contract & Downstream Asset Standards

These details are legacy compatibility guidance for users who explicitly request the older Google Flow Automator Max package. They are not required by the focused manga chapter asset workflow.

## 1. Full 30-File Flow Automator Max V3 Package

Every chapter produced for the legacy Google Flow Automator pipeline may generate the complete 30-file suite inside flow_queue/:

| Count | Pattern | Description |
|---|---|---|
| 6 | blockX_queue.csv | Single-row CSV for continuous 10s shot for Block X |
| 6 | blockX_frames_queue.csv | 6-row CSV for frame-by-frame shots in Block X |
| 6 | blockX_prompts.txt | Human-readable 11-part breakdown with timestamps |
| 6 | blockX_video_prompt.txt | Clean raw continuous prompt string for Block X |
| 1 | e0X.csv | Master episode CSV (6 continuous 10s blocks) |
| 1 | flow_continuous_10s_queue.csv | Mirror of continuous 10s blocks queue |
| 1 | flow_frame_by_frame_queue.csv | All 36 frame-by-frame shots in a single queue |
| 1 | flow_6_continuous_blocks.txt | All 6 continuous prompts separated by \\n\\n@@@NEXT@@@\\n\\n |
| 1 | flow_all_36_shots.txt | All 36 shot prompts separated by \\n\\n@@@NEXT@@@\\n\\n |
| 1 | char_refs_investor.csv | Character prompt queue for Slate/Flow model sheet generation |

### Flow CSV schema

prompt,description,hashtags,videoModel,videoMode,videoDurationSeconds,flowQuantity,videoVoiceReference,flowAspectRatio

## 2. Legacy visual filtering notes

- Treat translation-team banners, black padding buffers, reader credits, and end-of-chapter ads as non-narrative unless a human explicitly approves them.
- Do not filter by filename prefix alone; inspect image content and canonical scene classifications.
- The final freeze-frame beat must be explicit.
- Keep character identity references separate from storyboard collages.

## 3. Legacy language and timing

- Legacy default: six 10-second blocks and six timestamped beats per block.
- Voiceover emotion cues sit at the start of dialogue.
- The legacy Flow package is optional and title-specific scripts must not be mistaken for the generic chapter exporter.

