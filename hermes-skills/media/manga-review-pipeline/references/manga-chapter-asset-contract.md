# Manga Chapter Asset Contract

This is the focused contract for the requested asset pack. The old flow diagram is only a historical dependency sketch; it does not require parallel page readers or a manual video-generation handoff.

## Source panels

Store the ordered, untouched chapter pages under:

~~~text
<output>/<series-slug>/ch<chapter>/images/page_<number>.<ext>
~~~

Keep title, chapter number, source URL, fallback source, and page count in metadata.json. A panel is eligible for downstream visual assets only when it is a narrative page or a verified narrative crop. Exclude scanlation headers, reader credits, watermarks, end cards, advertisements, and unrelated promotional inserts.

## Character reference PNGs

Character sheets are identity anchors. For every recurring character used by the storyboard:

- output a PNG, normally 768x1376 (9:16);
- show front full body, 3/4 portrait, side profile, and seated/action view;
- keep face, hair, age, proportions, wardrobe, and signature props consistent;
- use a clean studio/model-sheet background and readable English name;
- do not include plot panels, speech bubbles, watermarks, or unrelated characters.

The first chapter creates the series reference set. Later chapters reuse it and record provenance in character_refs_source.json.

## Storyboard PNGs

Each block is a 9:16 director sheet matching the supplied storyboard example:

- black title header and black gutters;
- five rows: 2 + 1 + 2 + 2 + 1;
- six timing beats: 0s-1.5s, 1.5s-3s, 3s-4.5s, 4.5s-6s, 6s-8s, 8s-10s;
- the split rows contain distinct shots, not repeated crops;
- the last full-width beat ends on a complete freeze frame;
- no aggregator branding, warning cards, watermarks, or invented unrelated text.

Write metadata alongside the images:

~~~text
storyboard_9_16.json
storyboard_9_16.md
storyboard_9_16.html
nano_storyboards/block<nn>_<slug>.png
storyboard_assets_manifest.json
~~~

The storyboard sheet is a planning collage. Never use it as a video/image ingredient; use a clean, single-frame crop or character reference instead.

## Prompt TXT files

The primary prompt deliverable is plain text in flow_queue/:

~~~text
block1_prompts.txt
block2_prompts.txt
...
~~~

Each file contains the ordered beat prompts for one block, separated by:

~~~text
@@@NEXT@@@
~~~

A prompt must be grounded in storyboard JSON, begin with the 2D manhwa style lock, describe one full-bleed shot, preserve character-reference identity, carry action/camera/voice cues, and make the final beat a complete freeze frame. Keep prompts in English by default. CSV is not a substitute for these files.

The combined files flow_<N>_continuous_blocks.txt and flow_all_<shot-count>_shots.txt are optional convenience exports; they remain plain text and must agree with the per-block counts.

