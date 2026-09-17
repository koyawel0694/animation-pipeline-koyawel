# `/manga` Slash-Command Contract

This reference defines the user-facing command router for the `manga-review-pipeline` skill. The commands are agent-level workflow commands: Hermes should parse the request, run the appropriate local stages, and report verified artifacts.

## Command grammar

```text
/manga scrape [<manga-title-or-url>] <chapter>
/manga char <sensenova|antigravity> [<manga-title>] [<chapter>]
/manga storyboard <sensenova|antigravity> [<manga-title>] [<chapter>]
/manga blockprompts [<manga-title>] [<chapter>]
/manga help
```

Examples after a successful scrape has established the active chapter:

```text
/manga char sensenova
/manga storyboard antigravity
/manga blockprompts
```

Examples without an active chapter context:

```text
/manga scrape "The Investor Who Sees The Future" ch1
/manga char sensenova "The Investor Who Sees The Future" ch1
/manga storyboard antigravity "The Investor Who Sees The Future" ch1
/manga blockprompts "The Investor Who Sees The Future" ch1
```

Provider names are case-insensitive for parsing but should be normalized to lowercase. The only accepted image providers are `sensenova` and `antigravity`. `agy`, `auto`, and arbitrary provider names are invalid for these commands. A requested provider must be available in the Hermes environment; never silently fall back to a different provider.

## Active chapter context

Maintain these fields after a successful scrape or explicit chapter resolution:

```text
title
series_slug
chapter
chapter_dir
source_url
```

Resolve omitted arguments in this order:

1. Explicit arguments in the current command.
2. The active chapter context created earlier in the current task.
3. A single unambiguous chapter directory whose `metadata.json` matches the requested chapter.

If more than one chapter could match, ask for the title or an explicit chapter directory. If no context exists, do not infer a title from an unrelated folder or silently select the newest output.

## `/manga scrape`

Purpose: download and validate the source chapter only.

1. Resolve the title or URL and chapter using an authorized reader.
2. Run the scraper and create `output/<series-slug>/ch<chapter>/images/` and `metadata.json`.
3. Preserve ordered page files and record title, chapter, source URL, fallback source if used, and page count.
4. Mark or exclude warning cards, reader-credit pages, watermarks, and promotional inserts before downstream use.
5. Set the active chapter context only after metadata parses and page files are contiguous and readable.

Scrape does not claim that analysis, character references, storyboards, or prompts are complete. It should report the chapter directory so the next command can omit the title and chapter.

## `/manga char <provider>`

Purpose: create or reuse series-level character identity sheets.

1. Resolve the active chapter context.
2. Require a complete `chapter_analysis.json`; if it is missing, run the one sequential chapter reader for the whole chapter before generating images.
3. Reuse an established series `character_refs/` directory for later chapters. Generate only missing identity sheets with the requested provider.
4. For a new character, create a vertical `768x1376` PNG with front full body, 3/4 portrait, side profile, and seated or action pose. Keep face, hair, age, body proportions, wardrobe, skin tone, and signature props consistent.
5. Write or update `character_refs_source.json` with the reference directory, filenames, reuse status, provider, and generation provenance.
6. Verify every required PNG exists, opens, and has the expected dimensions before reporting success.

This command generates character identity assets, not storyboards or final video frames.

## `/manga storyboard <provider>`

Purpose: create a 10-second vertical storyboard block for each narrative block.

1. Resolve the active chapter context and require complete canonical analysis.
2. Require established character references. If references are missing, run the character-reference stage with the provider supplied to this command; do not invent identities from a partial page read.
3. Create `storyboard_9_16.json`, `storyboard_9_16.md`, and `storyboard_9_16.html` from the canonical analysis.
4. Generate or compose exactly one canonical storyboard PNG per block under `nano_storyboards/` using the requested provider or verified clean narrative crops.
5. Keep each block at exactly 10 seconds with these six beat windows unless the user explicitly requests a different supported layout: `0s-1.5s`, `1.5s-3s`, `3s-4.5s`, `4.5s-6s`, `6s-8s`, and `8s-10s`.
6. Make the final beat an explicit held pose/freeze frame. Do not use warning pages, promotional inserts, watermarks, or rejected storyboard variants.
7. Record provider and source-frame provenance in `storyboard_assets_manifest.json`, then verify dimensions, block count, beat count, and image readability.

A storyboard sheet is a planning artifact. It must not be passed to a video generator as a single video/image ingredient.

## `/manga blockprompts`

Purpose: export prompts for a video generator with a hard maximum of 10 seconds per block.

1. Resolve the active chapter context.
2. Require a validated `storyboard_9_16.json` and the character-reference provenance. If either is missing, stop and instruct the user to run `/manga storyboard <provider>` first.
3. Build prompts from the active storyboard JSON; never copy a different chapter's title, block names, page numbers, or dialogue.
4. Generate one `blockN_prompts.txt` per block with one full-bleed 9:16 shot prompt per beat separated by `@@@NEXT@@@`.
5. Generate one `blockN_video_prompt.txt` per block describing one coherent continuous clip of no more than 10 seconds. The default target is the user's Google Omni 1.1 Flash workflow; keep the model target as metadata or a prompt header, not as a reason to exceed the duration limit.
6. Also generate `flow_<N>_continuous_blocks.txt`, `flow_all_<shot-count>_shots.txt`, and `prompt_txt_manifest.json`.
7. Verify that every block is at most 10 seconds, every beat is represented, the delimiter count matches the beat count, and the manifest agrees with the storyboard JSON.

Do not make CSV the primary output. Create legacy CSV only when explicitly requested, in addition to the `.txt` files.

## Router behavior and errors

- `/manga help` prints the command grammar and short descriptions.
- An unknown command prints the supported commands and does not start a pipeline stage.
- A missing provider for `char` or `storyboard` is an error; ask the user to choose `sensenova` or `antigravity`.
- An unavailable requested provider is an error; do not silently substitute another API.
- A missing active chapter is an error; ask for a title and chapter or an explicit chapter directory.
- A failed prerequisite stops the command before image generation or prompt export and reports the missing path plus the next command to run.
- Completion reports must include the resolved chapter directory, provider used when applicable, block/beat counts, and verification result.
