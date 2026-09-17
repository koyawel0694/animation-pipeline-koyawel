# Manga Scraping and Canonical Analysis Contract

This contract defines Stage 1 of the manga video storyboard pipeline: acquiring clean, contiguous chapter pages and producing the single authoritative sequential narrative analysis.

## 1. Chapter Page Sourcing & Scraping

### Directory Layout
Chapter images must be saved into a dedicated directory:
```text
output/<series-slug>/ch<chapter-number>/images/
  page_001.webp (or .png, .jpg)
  page_002.webp
  ...
  page_NNN.webp
output/<series-slug>/ch<chapter-number>/metadata.json
```

### Scraping Rules
- **Contiguous numbering**: File names must follow strictly contiguous 1-indexed numbers (`page_001`, `page_002`, ...). Missing numbers or duplicate numbers are rejected.
- **Narrative pages only**: Strip reader credits, scanlation recruit cards, donation appeals, advertisements, and aggregator promotional inserts.
- **Source metadata**: `metadata.json` must record:
  ```json
  {
    "series_title": "The Investor Who Sees The Future",
    "series_slug": "the-investor-who-sees-the-future",
    "chapter": 1,
    "source_url": "https://...",
    "page_count": 23,
    "scraped_at": "2026-09-16T22:00:00Z"
  }
  ```
- **Scraper scripts in `~/manga-reviews/`**:
  - `manga_source_scraper.py`: Discovers manga chapters via MangaDex API or webtoon mirror fallbacks.
  - `scrape_manga.py`: Directly downloads pages from a given chapter URL.

## 2. Canonical Sequential Chapter Analysis

### Critical Sequential Rule
**NEVER analyze pages in parallel or out of order.** Splitting vision reading across parallel workers causes character names, pronouns, plot causality, and visual continuity to drift.

Always use a **single sequential reader** that analyzes page 1 to page N in chronological order, carrying forward scene context and character names from prior pages.

### Analysis Output Contract: `chapter_analysis.json`
Saved alongside the images:
```text
output/<series-slug>/ch<chapter-number>/chapter_analysis.json
```

Structure:
```json
{
  "chapter_title": "The Investor Who Sees The Future - Chapter 1",
  "series_slug": "the-investor-who-sees-the-future",
  "chapter_number": 1,
  "pages_analyzed": 23,
  "total_pages": 23,
  "pages": [
    {
      "page_number": 1,
      "page_file": "page_001.webp",
      "scenes": [
        {
          "scene_title": "Street Interview",
          "panel_location": "full-page",
          "speaker": "Street Reporter",
          "voice_emotion": "(energetic, professional broadcast tone)",
          "text_type": "spoken",
          "dialogue_text": "I ASKED THE CITIZENS OUT ON THE STREET!",
          "action_description": "High-angle shot of a busy pedestrian street in front of a cafe. Male reporter in a grey suit holds a microphone, while a cameraman and assistant film him.",
          "story_flow": "Establishes the public perception and viral speculation surrounding the mysterious fortune.",
          "video_animation_prompt": "Art style: authentic 2D Korean webtoon manhwa anime animation...",
          "camera_movement": "Slow crane down from high angle toward reporter",
          "visual_style_fx": "Bright daylight, realistic urban lighting",
          "estimated_duration_sec": 4.0
        }
      ]
    }
  ]
}
```

### Analysis Rules
- **Verbatim transcription**: Transcribe readable dialogue, narration boxes, and thoughts exactly. Never invent text.
- **Parenthesized emotion tags**: Tag vocal delivery inside parentheses: `(calm, restrained)`, `(shocked, trembling)`.
- **Visual facts only**: Describe visible actions, wardrobe, expressions, and blocking without speculating on unstated facts.
- **Text classification**: Mark readable text as `spoken`, `narration`, `thought`, `sfx`, `caption`, or `unknown` when possible. SFX such as onomatopoeia is not spoken dialogue.
- **Canonical script ledger**: After the analysis is saved, generate `chapter_script.json`, `chapter_script.txt`, and `chapter_script.md` deterministically from it. Preserve every non-empty `dialogue_text` in page/scene order, assign stable `p###-s##` IDs, and record the source-analysis hash. Never use a second model pass to rewrite or improve the transcript.
