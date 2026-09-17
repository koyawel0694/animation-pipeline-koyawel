# Multi-Chapter Run Example: Goblin's Ascent (Aug 17 2026)

## Source
MangaDex: https://mangadex.org/title/a958abd8-745d-4f47-9c4d-89abae30f5df
Title: "Goblin's Ascent: From Loser to Winner" / "From Goblin to Goblin God"
Genre: Dark Fantasy, Isekai, Reincarnation, Harem, Monsters

## Chapters Scraped
| Chapter | Pages | Analysis Time | Notes |
|---------|-------|---------------|-------|
| Ch 1 | 23 | 125s | Full chapter |
| Ch 2 | 28 (2x 404) | 159s | 2 pages failed (MangaDex CDN) |
| Ch 3 | 30 | 98s | Full chapter |

## Story Arc (3 chapters)
- **Ch1:** Goblin Chief dies, tribe collapses into chaos. Lin Tian (reincarnated human) stuck as weakling goblin, survives by staying low. Dark themes — captive adventurer, territorial fighting.
- **Ch2:** Lin Tian captured by humans, muzzled with spiked wire, interrogated by aristocratic blonde noblewoman. Golden arcane array ignites = evolution/power-up.
- **Ch3:** Now lethal — ambushes armed humans, kills a trafficker who offers bribes. Priestess/Saintess and sadistic hunter converging on his location.

## Narration Structure Used (v4, 184 words)
```
HOOK: "What if you woke up reborn as the lowest creature..."
PREMISE: "That's Goblin's Ascent. Lin Tian reincarnates not as some overpowered dragon lord, but as a goblin."
SPECIFIC SCENE: "There's this scene in chapter two where he's captured, muzzled with spiked wire..."
EVOLUTION: "Then the evolution hits. A golden arcane array ignites..."
ART: "The art is full-color manhwa — solid action panels..."
VERDICT: "Seven out of ten — still climbing."
```

## Curated Panels (10 selected from 81 total)
```
01_hook_eye.jpg      <- ch1 p27 (bloodshot eye close-up)
02_food_chain.jpg    <- ch1 p04 (cavern chaos)
03_ch2_title.jpg     <- ch2 p01 (chapter transition)
04_muzzled.jpg       <- ch2 p17 (muzzled goblin)
05_noblewoman.jpg    <- ch2 p19 (blonde aristocrat)
06_evolution.jpg     <- ch2 p27 (golden arcane array)
07_ambush.jpg        <- ch3 p07 (action slash)
08_bribe.jpg         <- ch3 p13 (bribe scene)
09_action.jpg        <- ch3 p08 (action highlight)
10_outro.jpg         <- ch1 p01 (title/cover)
```

## Output
- Video: ~/manga-reviews/output/review_goblin_v4.mp4
- 1080x1920, 71.9s, 12.7 MB, H.264+AAC
- TTS: en-US-GuyNeural via edge-tts (venv required)
- Ken Burns + 300ms fade transitions

## Key Learnings
1. Chapters 1-3 is the sweet spot for 60s TikTok — enough for authority, not enough to waste time
2. Curate panels manually from batch analysis — don't dump all pages
3. Write narration manually for multi-chapter — narrate.py can't synthesize across chapters
4. "There's this scene where..." beat is the single biggest improvement over generic synopsis
5. 184 words works for ~72s — slightly over 170-180 target but acceptable
