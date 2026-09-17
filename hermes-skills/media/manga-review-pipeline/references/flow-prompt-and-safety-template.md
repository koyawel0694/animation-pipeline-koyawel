# Google Flow 2D Manhwa Prompting & Policy-Safety Reference

## Proven 10-Second Continuous Scene Template

```text
@Character1 @Character2
Art style: authentic 2D Korean webtoon manhwa anime animation. Crisp clean dark ink line art, vibrant flat cel-shaded coloring, authentic manhwa character features, fluid 2D anime animation aesthetic. STRICTLY NOT 3D render, NOT live-action CGI, NOT photorealistic, NOT western comic book style. Full-bleed 9:16 vertical video. Smooth continuous animation across the 10-second sequence. Strictly NO comic panels, NO border frames, NO split screen, NO multi-panel collage, NO on-screen subtitles, NO speech bubbles, NO watermark.

SERYE DRAMA BLOCK — {Series Title} — Chapter {N} — Block {K} "{Block Title}" (10s, 6 beats)
INPUTS: attached image ingredients = faces of @Character1, @Character2 only (ref-locked). Animate strictly following the time-labeled beats below:

0s-1.5s — {BEAT_1_LABEL}: {Action description} · CAMERA: {Camera movement, lens} · LIGHTING: {Lighting details} · VO: ({Speaker}): "({emotion}) {Dialogue}" · SFX: {Sound effect}

1.5s-3s — {BEAT_2_LABEL}: {Action description} · CAMERA: {Camera movement, lens} · LIGHTING: {Lighting details} · VO: ({Speaker}): "({emotion}) {Dialogue}" · SFX: {Sound effect}

3s-4.5s — {BEAT_3_LABEL}: {Action description} · CAMERA: {Camera movement, lens} · LIGHTING: {Lighting details} · VO: ({Speaker}): "({emotion}) {Dialogue}" · SFX: {Sound effect}

4.5s-6s — {BEAT_4_LABEL}: {Action description} · CAMERA: {Camera movement, lens} · LIGHTING: {Lighting details} · VO: ({Speaker}): "({emotion}) {Dialogue}" · SFX: {Sound effect}

6s-8s — {BEAT_5_LABEL}: {Action description} · CAMERA: {Camera movement, lens} · LIGHTING: {Lighting details} · VO: ({Speaker}): "({emotion}) {Dialogue}" · SFX: {Sound effect}

8s-10s — {BEAT_6_LABEL} — END ON FREEZE FRAME: {Action description leading to locked pose} · CAMERA: {Final camera hold} · LIGHTING: {Lighting details} · VO: ({Speaker}): "({emotion}) {Dialogue}" · SFX: {Sound effect} · END ON COMPLETE FREEZE FRAME: {Character} holds locked pose and direct gaze motionless through 10s, zero extra movement.
```

## Policy Trigger Guardrails

| Forbidden Pattern | Reason | Safe Alternative |
| :--- | :--- | :--- |
| "Breaking news: crypto exchange collapses" | Triggers reputational risk / misinformation filter | "Fictional digital terminal displaying 'NETWORK OFFLINE / SERVERS UNREACHABLE'" |
| "Police cars outside headquarters", "CEO flees" | Triggers simulated real-world crime filter | "Online community forum feeds scrolling rapidly with frantic red alert icons" |
| "Photorealistic human skin pores, 4K film" | Destroys 2D anime style; causes 3D CGI drift | "Authentic 2D Korean webtoon line art, flat vibrant cel-shading" |
| Uploading multi-panel storyboard sheets as inputs | Makes Flow animate comic borders and text inside video | Use only single-frame crops from `clean_frame_crops/` or character reference sheets |
