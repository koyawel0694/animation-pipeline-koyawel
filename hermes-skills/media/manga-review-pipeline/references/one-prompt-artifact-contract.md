# One-Prompt Product Chapter Artifact Contract

Use after user requests a complete manga chapter product in one prompt.

## Required order

1. Source pages + metadata
2. `chapter_analysis.json`
3. `video_prompts.csv` + `pipeline_data.json`
4. `storyboard_9_16.json`, `.md`, `.html`
5. Established character reference resolution
6. Chapter-local `nano_storyboards/*.png`
7. Flow queue / production assets
8. Final artifact verification

## Character continuity

- First completed chapter for series creates character reference sheets.
- Later chapters use those existing sheets as known-character identity references.
- Reference sheets guide generation; they are not regenerated or copied into later chapter directories.
- Record provenance in `character_refs_source.json`.
- Preserve face, hair, wardrobe, age, body proportions, and recurring-character identity.

## Storyboard completion check

For each storyboard block, verify:

- PNG exists in chapter-local `nano_storyboards/`
- dimensions are vertical 9:16
- layout is 5 rows: `2 + 1 + 2 + 2 + 1`
- timestamps cover `0s-1.5s`, `1.5s-3s`, `3s-4.5s`, `4.5s-6s`, `6s-8s`, `8s-10s`
- final beat explicitly says freeze frame
- no scanlation warning, aggregator promotion, watermark, or unrelated text

## Recovery

If model-generated storyboard sheets time out, do not report failure after leaving metadata only. Use approved clean narrative crops and a deterministic compositor, then verify all PNGs. Never use known promotional/warning inserts as visual source frames.
