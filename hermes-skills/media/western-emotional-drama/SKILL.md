---
name: western-emotional-drama
description: "Create prompt-only Western emotional-drama packages."
version: 2.1.0
author: John, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [western, emotional-drama, prompt-pipeline, google-flow, serialized-video]
    category: media
    related_skills: [ai-drama-series-pipeline, ai-video-pipeline]
---

# Western Emotional Drama Skill

Use this skill to turn an original Western emotional-drama premise into a continuity-safe, copy-paste-ready prompt package for Google Flow. It applies the supplied audited v2.1 pipeline: one 30-second episode is one coherent dramatic scene made from three consecutive 10-second cinematic micro-sequences. Each micro-sequence may contain 2–5 motivated shots; do not force the whole episode into one physical camera take.

The complete V2.1 source is preserved verbatim in `references/western-emotional-drama-pipeline.md`. Load that reference for the detailed prompt templates, camera grammar, episode contracts, Flow notes, and quality checklist.

This skill is prompt-only: it plans and writes production artifacts, but it does not operate Google Flow or guarantee that a particular Flow model or feature is available in the user's account. No code-generation requirement is part of the creative output contract.

## When to Use

- Create or extend an original serialized Western emotional-drama series.
- Build a series bible, episode storyflow, character/location/prop references, or voice profiles.
- Generate the cinematic shot blueprint and exactly three 10-second Google Flow prompts for an episode.
- Design hooks, emotional turns, cliffhangers, replay/loop images, dialogue, sound, or period-correctness constraints.
- Repair continuity, screen geography, camera motivation, performance, prompt conflict, or retention problems.
- Audit a prompt package before rendering.

Do not use this as a generic video-editing workflow, a code-generation workflow, or for unrelated UGC/product clips; use the matching media skill instead.

## Originality and Safety Boundary

Create original material. Do not adapt, paraphrase, imitate, or reproduce an existing film, television series, novel, comic, or copyrighted character. Preserve the requested Western period and drama without adding arbitrary spectacle or gratuitous violence. If a scene involves harm, keep the prompt focused on story consequence, implication, reaction, and safe cinematic depiction rather than graphic detail.

## Inputs to Collect

Ask for or infer only what is missing:

- series premise, title, tone, era, geography, and chosen visual style;
- protagonist wound/desire, secondary character, relationship, conflict, secret, promise, midpoint reversal, final choice, payoff, and motif;
- character names, ages, appearance, wardrobe anchors, relationships, voice profiles, and performance direction;
- location architecture, time window, weather, motivated lighting, props, and visual motif;
- episode purpose, emotional start/end, central question, one dramatic event, new information, emotional turn, final image, and next-episode question;
- exact dialogue or no dialogue, language, diegetic sound, music constraints, and available voice/reference images;
- any reference videos/images and whether the user wants prompts only, a Flow-ready text export, or an actual render/QC workflow.

## Core Contract

- Prompt-only output; return the requested prompt artifacts rather than a production essay.
- Default production target: Gemini Omni Flash 1.1, 30 seconds total, exactly 3 generations, 10 seconds each, vertical 9:16. Verify the active Flow interface because features and availability can change.
- Each 10-second generation is a cinematic micro-sequence. Use approximately 2–5 motivated shots when needed; one shot is valid when it is more powerful and coherent.
- The three generations are consecutive dramatic beats in one coherent scene, not unrelated clips and not a random montage.
- Keep one location, one time window, one primary emotional event, one central question, one important change, and one ending question whenever the story permits.
- Prefer 1–2 primary characters and 0–1 dominant prop per episode.
- The first second must contain narrative information. The final generation must answer one small question and create one larger, specific question.
- Treat supplied character, location, prop, and voice images as canonical references. Written prompts must complement, never contradict, them.
- Preserve character identity, wardrobe, location, props, time, lighting, weather, emotional state, screen geography, and visual style across all three generations.
- Every shot and camera move needs story information, emotional purpose, or a meaningful transition.

## Procedure

1. Load `references/western-emotional-drama-pipeline.md` when detailed wording is needed. Use Sections 0–7 and 43–49 for the governing architecture and Sections 8–42 for reusable prompts. Completion criterion: the plan follows V2.1's micro-sequence model rather than V2.0's one-take interpretation.
2. Establish or update the series bible before episode prompts. Determine the minimum episode count required by the emotional arc; 6–12 is preferred only when justified. Completion criterion: the story has a clear relationship, conflict, emotional engine, endpoint, and no filler episodes.
3. Build canonical character, expression/performance, location, prop, motif, and voice-reference prompts. Completion criterion: recurring identities and world details are stable enough to reuse.
4. Define the episode storyflow: purpose, location, time window, characters, dominant prop, emotional start/end, central question, one major event, new information, reversal/turn, final image, and next question. Completion criterion: one answer, one emotional change, and one necessary next-episode question are explicit.
5. Apply the retention scaffold as flexible guidance: 0–2 seconds hook, 2–5 question/dialogue, 5–8 reaction, 8–10 mini-turn; then information/response/pressure/reveal; finally consequence, emotional close-up, story-critical detail, and cliffhanger. Completion criterion: every generation changes the dramatic state without overloading the timing.
6. Design the cinematic shot blueprint before writing the final Flow prompts. For each necessary shot specify time range, size, angle, height, lens language, position, movement, focus, blocking, facial performance, prop, lighting, composition, dialogue, diegetic sound, purpose, and transition. Completion criterion: every cut and camera choice has a reason.
7. Record continuity states B0, B1, B2, and B3. B0 is the episode beginning; B1, B2, and B3 describe the end state of generations 01, 02, and 03. These are continuity states, not necessarily single camera frames. Use start/end frame anchors when the active Flow workflow supports them. Completion criterion: each next generation can begin without inventing a new scene.
8. Generate exactly three micro-sequence prompts: Generation 01 = hook + character + question; Generation 02 = pressure + new information + reaction; Generation 03 = consequence + emotional turn + reveal + cliffhanger. Completion criterion: each prompt has a clear start state, end state, motivated shots, and no unrelated action.
9. Apply the prompt-precedence order: story truth; canonical references; previous-block continuity; blocking; editing structure; camera/lens/movement; lighting; atmosphere; audio; style polish. Completion criterion: lower-priority style language cannot contradict higher-priority story or continuity.
10. Apply dialogue, emotional-performance, lighting/atmosphere, period-correctness, negative/error-guard, voice-continuity, and audio-design rules. Completion criterion: vague words such as “cinematic” or “emotional” have been converted into observable camera, movement, performance, lighting, composition, timing, or sound instructions.
11. If the user requests rendering, hand the approved prompts to the appropriate browser or Flow automation workflow. Use available references, ingredients, start/end frames, voice references, or video editing features without making the package depend on an optional feature. Completion criterion: the generated clips remain usable if a listed feature is unavailable.
12. Run the continuity guard and final video-prompt auditor before approval. Completion criterion: every failed check has a concrete rewritten prompt or an explicit user decision.

## Camera and Editing Rules

- A 10-second generation normally uses 2–5 shots, but shot count is subordinate to clarity.
- Specify shot size, angle, height, lens, position, movement, focus, composition, and blocking when they affect the result.
- Motivate movement: push in for realization/intimacy; pull back for isolation/loss; track for movement/pursuit; arc for revelation; lock off for truth/grief; controlled handheld for instability; rack focus for an attention shift.
- Cut for new information, a meaningful reaction, a new point of view, emotional emphasis, or spatial clarification—not merely for visual variety.
- Preserve the 180-degree axis, left/right relationships, eye-lines, walking direction, and recognizable location geometry.
- Keep the last two seconds visually simple when possible so the final image and cliffhanger read clearly.
- Do not request several unrelated scenes, flashbacks, time-lapse, or a generic “AI montage” inside one generation.

## Deliverable Format

Unless the user requests another format, return only the requested prompt artifacts in this logical order:

1. `00_story_blueprint.txt`
2. `01_character_reference_prompts.txt`
3. `02_location_reference_prompts.txt`
4. `03_prop_reference_prompts.txt`
5. `04_camera_shot_blueprint.txt`
6. `05_generation_01_flow_prompt.txt`
7. `06_generation_02_flow_prompt.txt`
8. `07_generation_03_flow_prompt.txt`
9. `08_continuity_guard.txt`
10. `09_final_audit.txt`

Optional series-level artifacts are `series_master_prompt.txt`, `visual_style_anchor.txt`, and `character_voice_profiles.txt`. No storyboard collage or CSV is required for the creative prompt layer. For Flow Automator ingestion, offer a plain-text export on request, preserve prompt boundaries exactly, and use `@@@NEXT@@@` separators when that is the user's established import format.

## Example Requests

- “Use the western-emotional-drama skill to create an original Episode 1 from this premise: …”
- “Build the series bible and six-to-twelve-episode storyflow for this Western emotional arc.”
- “Create the shot blueprint, B0–B3 continuity states, and exactly three 10-second Flow micro-sequence prompts for this train-station farewell.”
- “Generate 12 first-second hooks and select the one that communicates the most story with the least exposition.”
- “Audit these three generation prompts for identity, screen geography, camera motivation, and cliffhanger continuity.”
- “Export the approved package as Flow-ready `.txt` files with `@@@NEXT@@@` separators.”

## Verification

Before calling a package complete, confirm all of the following:

- exactly three 10-second generations are present;
- each generation is a coherent micro-sequence, usually 2–5 motivated shots rather than random montage;
- B0/B1/B2/B3 continuity states and both generation handoffs are explicit;
- one dramatic event, one emotional change, and one specific next question are present;
- the shot blueprint gives camera choices a narrative reason;
- character, location, prop, voice, lighting, weather, period, and screen geography remain consistent;
- prompts do not contradict supplied references or assume unavailable Flow features;
- the output contains no code, filler essay, arbitrary spectacle, unrelated location, modern period errors, embedded subtitles, logos, or watermark instructions;
- the final audit marks every critical item PASS or supplies a concrete revision.

The linked V2.1 reference remains authoritative if this wrapper and the original pipeline ever differ.
