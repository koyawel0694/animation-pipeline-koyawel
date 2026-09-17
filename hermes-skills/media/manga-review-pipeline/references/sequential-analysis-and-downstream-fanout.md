# Sequential Analysis + Downstream Fan-Out

Validated workflow for chapter image processing.

## Why page analysis stays sequential

One reader must carry continuity across pages. Independent vision workers may produce incompatible names, speaker attribution, chronology, emotional tone, or visual identity. Speed gain is not worth story drift.

## Stage 1: canonical reader

Run one worker across pages in filename order:

```bash
/home/john/.venv_manga/bin/python3 sequential_chapter_analysis.py \
  --chapter-dir /home/john/manga-reviews/output/<series>/ch1
```

Use direct Antigravity CLI with `--effort medium`. Save after each page. Output schema:

```json
{
  "title": "...",
  "chapter": "1",
  "analysis_mode": "single sequential reader",
  "agy_effort": "medium",
  "pages_analyzed": 23,
  "total_pages": 23,
  "pages": [
    {
      "page_number": 1,
      "page_file": "page_001.webp",
      "scenes": [
        {
          "scene_title": "...",
          "speaker": "...",
          "voice_emotion": "(emotion, tone)",
          "dialogue_text": "exact readable text",
          "action_description": "visible action",
          "story_flow": "continuity note",
          "video_animation_prompt": "initial motion guidance",
          "camera_movement": "...",
          "visual_style_fx": "...",
          "estimated_duration_sec": 4.0
        }
      ]
    }
  ]
}
```

Do not downstream fan out until all pages are present and JSON parses.

## Stage 2: safe parallel work

Prompt worker and storyboard worker may run simultaneously because both read identical canonical JSON:

- Prompt worker: preserve exact dialogue and page/scene IDs; write CSV + pipeline JSON.
- Storyboard worker: create one beat per canonical scene; include 9:16 safe zones, visual anchor, environment plate, camera cue, VO, SFX, BGM, and manual recipe.

Workers must not reread images or invent plot facts. Recommendations such as SFX/BGM may be creative, but mark them as production recommendations, not source facts.

## Final validation

Check:

1. `pages_analyzed == total_pages`.
2. Page numbers contiguous from 1 through total.
3. Every output page filename exists in canonical analysis.
4. Scene IDs contiguous and ordered.
5. CSV row count equals canonical scene count.
6. Storyboard beat count equals canonical scene count.
7. Dialogue text matches canonical source after emotion-prefix formatting.
8. JSON, CSV, Markdown, and HTML files exist and parse/render.

## Source fallback

MangaDex can contain metadata and an English title while exposing zero downloadable chapters. For a test title, first check MangaDex feed. If empty, use a legal/authorized reader source adapter rather than passing unsupported `translatedLanguage[]=raw`; MangaDex returns HTTP 400 for that value. Preserve source URL in chapter metadata and record fallback provenance.
