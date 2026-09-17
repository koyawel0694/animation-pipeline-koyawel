---
name: manga-review-pipeline
description: "Use when turning a manga/manhwa/manhua chapter into panel assets, character-reference sheets, 9:16 storyboards, block prompt .txt files, or handling the /manga slash-command workflow."
license: MIT
metadata:
  hermes:
    tags: [manga, manhua, manhwa, panels, character-references, storyboards, prompts]
    category: media
    related_skills: [ai-video-content-qa, ai-video-format-replication]
---

# Manga Chapter Asset Pipeline

## Overview

Use this skill to turn one manga/manhwa/manhua chapter into a verified production asset pack:

1. ordered chapter panels plus source metadata;
2. one canonical sequential chapter analysis;
3. a canonical exact-text script ledger with stable source-scene IDs;
4. series-level character reference PNGs;
5. 9:16 storyboard metadata (optional storyboard-sheet PNGs only when explicitly requested);
6. one plain-text prompt file per storyboard block, plus combined plain-text prompt files.

This is an asset-preparation workflow. It does not require rendering a final TikTok video, narration audio, subtitles, or a CSV queue. Treat CSV/Flow automation as legacy compatibility only when the user explicitly asks for it.

The working checkout is normally ~/manga-reviews/. The Hermes source copy is normally ~/Documents/Obsidian Vault/hermes-skills/media/manga-review-pipeline/; the installed runtime copy is normally ~/.hermes/skills/media/manga-review-pipeline/. Keep both copies aligned when editing this skill.

## When to Use

Use for requests such as:

- scrape or download a manga/manhwa/manhua chapter's panels;
- make character reference/model sheets from a chapter or series;
- create SERYE-style vertical storyboard sheets;
- produce block prompts as .txt files for later image/video generation;
- package the above outputs for a manga/manhwa/manhua adaptation.

Do not activate this workflow only to write a generic manga review, make a final narrated slideshow, or edit an already-rendered video.

## Slash command interface

Treat a user message beginning with `/manga` as a command request and route it using [references/slash-command-contract.md](references/slash-command-contract.md).

The supported commands are:

~~~text
/manga scrape [manga-title-or-url] <chapter>
/manga char <sensenova|antigravity> [manga-title] [chapter]
/manga storyboard <sensenova|antigravity> [manga-title] [chapter]
/manga blockprompts [manga-title] [chapter]
~~~

For `char`, `storyboard`, and `blockprompts`, an omitted title or chapter resolves to the active chapter context established by a successful scrape in the current task. Do not guess between multiple titles or chapters. `sensenova` and `antigravity` are the only valid image-generation providers for `char` and `storyboard`; do not silently substitute `agy`, `auto`, or another provider. If the requested provider is unavailable, stop and report the configuration problem.

The command workflow is stateful within the task: scrape establishes the title, slug, chapter, source URL, and chapter directory; downstream commands reuse that context. Every command must still verify its prerequisite files and report the exact output directory when complete.

## Non-negotiable workflow rules

- Use an authorized or user-provided source. Preserve the source URL and chapter identity in metadata.
- Read pages in filename order and keep the downloaded page files unchanged as the source layer.
- Use one sequential vision reader for a chapter. Do not split page ranges among parallel readers; that causes character, chronology, and dialogue drift.
- Fan out only after the canonical analysis is complete. Prompt, storyboard, and asset workers may read the same validated JSON, but they must not independently reinterpret the source pages.
- Reuse established series character references for later chapters. Do not regenerate or copy a new identity sheet on every chapter.
- Keep the storyboard sheet separate from individual Flow/image ingredients. A storyboard is a planning collage; a generated shot should be a single full-bleed frame.
- Default all generated prompt text, dialogue, emotion cues, labels, and metadata descriptions to natural English unless the user explicitly requests another language.
- Never claim an artifact exists from a log message alone. Verify its file path, dimensions, count, and parseability before reporting completion.

The old flow diagram supplied with this skill is historical context only. It may explain the broad stages, but it is not a requirement to spawn three page-analysis workers or to recreate its manual-video step.

## Pipeline stages

### 1. Scrape the chapter panels

Resolve the title or URL, select the requested chapter count, and write each chapter under:

~~~text
output/<series-slug>/ch<chapter>/
  images/page_001.<ext>
  metadata.json
~~~

Use manga_source_scraper.py for MangaDex discovery and its reader fallback. If a source exposes title metadata but no readable MangaDex pages, record the fallback source and stop if no authorized reader is available; do not invent a URL or silently mix sources.

Completion evidence:

- images/metadata.json exists and parses;
- page filenames are ordered and contiguous;
- every listed panel exists and can be opened;
- metadata.json records the title, chapter, source URL, and downloaded page count;
- scanlation splash pages, reader credit cards, and promotional inserts are marked or excluded from downstream narrative assets.

### 2. Build the canonical analysis

Run the sequential reader once for the complete chapter:

~~~bash
cd ~/manga-reviews
source ~/.venv_manga/bin/activate
python3 sequential_chapter_analysis.py \
  --chapter-dir output/<series-slug>/ch<chapter>
~~~

It writes chapter_analysis.json. The analysis must retain ordered page filenames, visible scenes, exact readable dialogue, speakers, emotions, actions, continuity notes, and prompt-safe camera/style observations. It saves progress so an interrupted run can resume; retry the failed page instead of restarting or merging independent analyses.

After analysis, generate `chapter_script.json`, `chapter_script.txt`, and `chapter_script.md` deterministically from the saved JSON. Preserve every non-empty `dialogue_text` in page/scene order, assign stable `p###-s##` IDs, retain speaker and delivery, and mark SFX as not spoken. This ledger is the only script source for storyboard and prompt stages.

Do not start downstream asset work until:

~~~text
pages_analyzed == total_pages
page numbers are contiguous
chapter_analysis.json parses as JSON
every analyzed page filename exists in images/
~~~

### 3. Create character reference sheets

Character references are identity anchors, not storyboards. For the first completed chapter of a series, generate one 9:16 PNG model sheet per recurring character using the character facts supported by the canonical analysis. Each sheet should show the same character in four consistent views:

- front full body;
- 3/4 portrait;
- side profile;
- seated or action pose.

Lock face, hair, age, body proportions, skin tone, wardrobe, and signature props across all views. Use a clean studio background, clear character name, no plot scene, no speech bubbles, and no extra characters.

Expected output:

~~~text
<series-root>/ch1/character_refs/
  <character>_ref.png
character_refs_source.json
~~~

Use the existing series character_refs/ as the reference directory for later chapters. Record the source directory and reused filenames in character_refs_source.json; a provenance manifest is required even when no new PNG is generated.

Completion evidence:

- at least one PNG exists for every recurring character needed by the storyboard;
- PNGs are readable and vertical 9:16 (the local contract uses 768x1376);
- every reference contains multiple consistent views rather than a single plot frame;
- later chapters point to established refs instead of silently regenerating them.

### 4. Create the storyboard metadata and optional image sheets

First create the machine-readable and human-readable storyboard:

~~~bash
python3 build_serye_storyboard.py \
  --analysis output/<series-slug>/ch<chapter>/chapter_analysis.json \
  --output-dir output/<series-slug>/ch<chapter>
~~~

Storyboard-sheet PNGs are optional and only run when explicitly requested. If requested, create them from approved clean narrative crops or a verified image-generation pass. The local compositor command is:

~~~bash
python3 compose_chapter_storyboards.py \
  --chapter-dir output/<series-slug>/ch<chapter> \
  --reference-dir output/<series-slug>/ch1/character_refs
~~~

Use generate_nano_storyboards.py for first-time character sheets or optional model-generated storyboard art. If the compositor is used, verify that clean_frame_crops/ contains approved narrative frames first; never fill it with a scanlation banner, reader credit, or unrelated promotional card.

The storyboard-sheet visual contract follows the supplied storyboard example:

- vertical 9:16 canvas, normally 768x1376;
- black header and gutters with a concise English title;
- five rows laid out 2 + 1 + 2 + 2 + 1;
- six timestamped beats: 0s-1.5s, 1.5s-3s, 3s-4.5s, 4.5s-6s, 6s-8s, 8s-10s;
- split rows show distinct shots, not duplicated crops;
- the final full-width beat is an explicit held pose/freeze frame;
- no watermark, aggregator branding, warning card, or invented unrelated text.

Required output:

~~~text
storyboard_9_16.json
storyboard_9_16.md
storyboard_9_16.html
chapter_script.json / .txt / .md
~~~

Optional storyboard-sheet output, when explicitly requested:

~~~text
nano_storyboards/block<nn>_<slug>.png
storyboard_assets_manifest.json
~~~

A storyboard image is a director's blueprint. Never attach the multi-panel sheet as a video/image ingredient; use a clean single-frame crop or a character reference instead.

### 5. Export block prompts as plain text only

The requested prompt deliverable is plain text. Build it from storyboard_9_16.json, not from a stale hardcoded title script:

~~~bash
python3 build_block_prompts_txt.py \
  --chapter-dir output/<series-slug>/ch<chapter>
python3 verify_manga_chapter_assets.py \
  --chapter-dir output/<series-slug>/ch<chapter>
~~~

Expected output in flow_queue/:

~~~text
block1_prompts.txt
block1_video_prompt.txt
...
blockN_prompts.txt
blockN_video_prompt.txt
flow_<N>_continuous_blocks.txt
flow_all_<shot-count>_shots.txt
prompt_txt_manifest.json
~~~

Each blockN_prompts.txt contains one shot prompt per beat separated by:

~~~text
@@@NEXT@@@
~~~

Each prompt must describe one full-bleed 9:16 shot, preserve the reference-sheet identity, carry the beat's action/camera/script cue, and include the explicit final freeze-frame instruction on the last beat. Both the shot prompt and continuous `blockN_video_prompt.txt` must contain the exact canonical cue for every beat. Use an explicit no-dialogue cue for silent/transition beats, mark SFX as not spoken, and never invent, paraphrase, repeat, or move dialogue. Follow the confirmed style preset and forbid comic borders, split screens, subtitles, speech bubbles, watermarks, and storyboard-inside-storyboard output.

Do not make CSV the primary deliverable for this workflow. If a user explicitly requests the legacy Flow Automator CSV, generate it in addition to—not instead of—the .txt files and verify the documented schema separately.

## One-shot recipe

For an existing chapter directory:

~~~bash
cd ~/manga-reviews
source ~/.venv_manga/bin/activate
python3 manga_pipeline.py \
  --existing-dir output/<series-slug>/ch<chapter> \
  --stage all
python3 build_block_prompts_txt.py \
  --chapter-dir output/<series-slug>/ch<chapter>
~~~

If upstream artifacts already exist, reuse them. Run only the missing stage when possible. If the orchestrator's local checkout contains uncommitted or title-specific legacy scripts, run the stage commands explicitly and keep the generic build_block_prompts_txt.py exporter as the source for plain-text prompts.

For a new title, use --title or --url with --chapters 1, then locate the exact chapter directory from the scraper output before running downstream commands.

## References

Read only the reference needed for the current branch:

- references/slash-command-contract.md — parse `/manga` commands, resolve active chapter context, enforce provider selection, and route prerequisites.
- references/manga-chapter-asset-contract.md — exact artifact names, image dimensions, storyboard layout, and TXT delimiter contract.
- references/sequential-analysis-and-downstream-fanout.md — canonical reader schema, safe fan-out boundary, and validation.
- references/one-prompt-artifact-contract.md — completion order and character-reference provenance.
- references/manhua-flow-video-generation.md — read only when the user asks how to use a storyboard or crop in a video generator.
- references/chapter_production_contract.md — legacy Flow package details; use only when CSV/queue compatibility is explicitly requested.

## Common pitfalls

1. Stopping at analysis or CSV. The requested product includes the canonical script ledger and verified block .txt files; storyboard PNG sheets are optional. Check every required output path.
2. Parallel page readers. Use one sequential reader; parallelize only downstream transformations after canonical JSON is complete.
3. Regenerating known characters. Reuse the series reference directory and write provenance.
4. Uploading a storyboard collage. The collage contains borders, timestamps, and multiple shots; use a clean crop or model sheet as an ingredient.
5. Using promotional source art. Exclude scanlation headers, reader credits, watermarks, and end cards from narrative crops.
6. Hardcoded chapter prompts. Build prompt text from the active chapter's storyboard JSON; never reuse the Investor example's block names or page numbers for another title.
7. Claiming a generated image exists. Inspect dimensions and open the file before reporting it.
8. Language drift. Keep prompt, VO, and labels in English by default; only switch languages on explicit request.
9. Script drift. Treat `chapter_script.json` as canonical, validate its source hash, and reject prompts whose script cue or source-scene ID does not match the saved analysis.

## Verification checklist

- [ ] Source URL, title, chapter, page count, and provenance are recorded.
- [ ] Every downloaded panel exists, opens, and is in the expected order.
- [ ] chapter_analysis.json parses and has complete contiguous page coverage.
- [ ] chapter_script.json, chapter_script.txt, and chapter_script.md preserve every non-empty source text entry with stable IDs.
- [ ] character_refs/ contains the required PNG identity sheets and character_refs_source.json.
- [ ] storyboard_9_16.json, .md, and .html exist and agree on block/beat counts.
- [ ] flow_queue/blockN_prompts.txt exists for every block, contains the @@@NEXT@@@ delimiter between shots, and contains no CSV-only substitution.
- [ ] Every continuous block prompt contains the exact canonical script cue for each beat; SFX is not spoken and transitions contain no dialogue.
- [ ] Combined TXT files and prompt_txt_manifest.json report the same block and shot counts as the storyboard JSON.
- [ ] verify_manga_chapter_assets.py exits successfully for the completed chapter.
- [ ] No storyboard collage, scanlation insert, watermark, or promotional card is being used as a video ingredient.
