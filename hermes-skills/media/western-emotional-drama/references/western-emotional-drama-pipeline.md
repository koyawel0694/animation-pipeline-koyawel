# WESTERN EMOTIONAL DRAMA - HERMES PROMPT PIPELINE
## Audited v2.1 - Reference-Aligned Cinematic Micro-Drama Architecture
### Prompt-only production system for 30-second serialized Western drama in Google Flow with Gemini Omni Flash 1.1

---

## 0. WHAT CHANGED IN v2.1

This revision incorporates the actual visual language of the supplied reference videos.

The earlier v2.0 treated each 10-second generation too much like a single continuous camera take. That is **not** the target style.

The reference style is better described as:

```text
30-SECOND CINEMATIC MICRO-DRAMA
        |
        +-- 10s GENERATION 01
        |     multiple motivated shots
        |
        +-- 10s GENERATION 02
        |     multiple motivated shots
        |
        +-- 10s GENERATION 03
              multiple motivated shots
```

Each 10-second generation is therefore a **micro-sequence**: a short chain of cinematic shots that together advances one dramatic beat.

The three generations still belong to one episode and must maintain:

- canonical character identity;
- wardrobe continuity;
- location continuity;
- time continuity;
- prop continuity;
- emotional continuity;
- screen geography;
- visual style.

The key creative correction is:

> **Do not force the entire 30-second episode into one physical camera take. Design it as one coherent dramatic scene made from short, purposeful cinematic shots.**

---

# 1. CORE OBJECTIVE

Create an original serialized Western drama that feels like a real short scene from a prestige live-action film, but is optimized for short-form retention.

The system is prompt-only. Its principal outputs are:

```text
character-reference prompts
location-reference prompts
prop-reference prompts
series/storyflow prompts
episode blueprint prompts
camera-direction prompts
10-second Google Flow video prompts
continuity prompts
prompt audit prompts
```

No code-generation requirement is part of the creative output contract.

The system must make the audience:

```text
STOP
  ->
CARE
  ->
QUESTION
  ->
WORRY
  ->
FEEL
  ->
NEED THE NEXT EPISODE
```

No system can guarantee millions of views. The pipeline instead optimizes for immediate narrative clarity, emotional attachment, strong visual storytelling, serialized curiosity, and repeatable production quality.

---

# 2. GOOGLE FLOW PRODUCTION TARGET

## Locked default

```text
MODEL:
Gemini Omni Flash 1.1

EPISODE:
30 seconds

GENERATIONS:
3

GENERATION LENGTH:
10 seconds each

FORMAT:
9:16 vertical

OUTPUT:
3 separate 10-second micro-sequences joined into one 30-second episode
```

Google's current Flow documentation lists Gemini Omni Flash 1.1 with Text to Video, First Frame, First + Last Frames, Ingredients/References to Video, and video-to-video editing up to 10 seconds. It also lists 10-second generations for these video modes. Feature availability can vary by region and interface, so prompts must remain usable without depending on one optional feature. See Section 26 for source links.

Important implementation principle:

**The prompt system must be compatible with both:"

```text
REFERENCE-DRIVEN FLOW WORKFLOW
AND
TEXT-DRIVEN FLOW WORKFLOW
```

When reference/frame inputs are available, use them as the identity and continuity source of truth.

---

# 3. THE ACTUAL EPISODE ARCHITECTURE

Every 30-second episode is one **dramatic scene** rather than one uninterrupted take.

```text
EPISODE
30 seconds

10s MICRO-SEQUENCE 01
HOOK + QUESTION

10s MICRO-SEQUENCE 02
PRESSURE + INFORMATION

10s MICRO-SEQUENCE 03
REACTION + REVEAL + CLIFFHANGER
```

Each micro-sequence may contain approximately 2-5 shots, depending on story density.

The exact number is not sacred.

The rule is:

> **Every shot exists to deliver story information, character emotion, or a meaningful visual transition.**

Do not add shots simply to make the video look cinematic.

---

# 4. 30-SECOND RETENTION FORMULA

Default rhythm:

```text
0-2s    VISUAL HOOK
2-5s    QUESTION / DIALOGUE
5-8s    REACTION
8-10s   MINI TURN

10-13s  NEW INFORMATION
13-16s  CHARACTER RESPONSE
16-18s  CONFLICT / PRESSURE
18-20s  MINI REVEAL

20-23s  CONSEQUENCE
23-26s  EMOTIONAL CLOSE-UP
26-28s  IMPORTANT VISUAL DETAIL
28-30s  CLIFFHANGER / NEXT QUESTION
```

This is a flexible timing scaffold, not a rigid edit.

The emotional information is more important than exact second marks.

---

# 5. STORY RULE: ONE DRAMATIC EVENT PER EPISODE

A 30-second episode should generally contain:

```text
ONE LOCATION
ONE TIME WINDOW
ONE PRIMARY EMOTIONAL EVENT
ONE CENTRAL QUESTION
ONE IMPORTANT CHANGE
ONE ENDING QUESTION
```

Use 1-2 primary characters whenever possible.

Avoid:

- long travel sequences;
- five-character introductions;
- multiple unrelated locations;
- complicated exposition;
- several unrelated conflicts;
- filler dialogue;
- spectacle without emotional purpose.

The audience should understand the episode even when the subject matter is mysterious.

---

# 6. SERIES-LENGTH ENGINE

Do not force every story into a fixed episode count.

The Story Architect determines the minimum number of 30-second episodes required to complete the emotional arc.

Preferred range:

```text
6-12 episodes
```

But the actual count may be shorter or longer when the story requires it.

An episode is justified when it advances:

```text
character relationship
or
central mystery
or
stakes
or
emotional transformation
or
causal chain
```

Delete episodes that only:

```text
repeat information
travel
stall
summarize
add filler conflict
```

The final episode must resolve the central emotional question and the central relationship arc.

---

# 7. EMOTIONAL STORY ENGINE

The emotional sequence should usually resemble:

```text
CURIOSITY
   ->
ATTACHMENT
   ->
UNEASE
   ->
PRESSURE
   ->
DISCOVERY
   ->
REACTION
   ->
EMOTIONAL TURN
   ->
NEW QUESTION
```

Do not force every episode to end in sadness.

Useful emotional engines include:

```text
loss
sacrifice
fatherhood
motherhood
loyalty
betrayal
forgiveness
regret
love
separation
reunion
redemption
promise
justice
secrets
```

The Western world supplies atmosphere and stakes.

The relationship supplies the emotional meaning.

---

# 8. MASTER SERIES ARCHITECT PROMPT

```text
You are the SHOWRUNNER and STORY ARCHITECT for an original serialized Western emotional
drama designed for 30-second vertical video episodes.

Create ORIGINAL material. Do not adapt, paraphrase, imitate, or reproduce an existing
movie, television series, novel, comic, or copyrighted character.

The storytelling should feel like a dramatic scene from a prestige live-action Western
feature film, but optimized for short-form retention.

CORE PRINCIPLE:
The Western setting supplies atmosphere and scale.
The human relationship supplies the emotional meaning.

BUILD:
SERIES TITLE
LOGLINE
CENTRAL THEME
PROTAGONIST
PROTAGONIST WOUND
PROTAGONIST DESIRE
SECONDARY CHARACTER
RELATIONSHIP
CENTRAL CONFLICT
SECRET
PROMISE
MIDPOINT REVERSAL
FINAL CHOICE
FINAL PAYOFF
FINAL VISUAL MOTIF

Then determine the minimum number of 30-second episodes required to tell the story
without filler.
Preferred range: 6-12 episodes, but use another number if justified by the story.

FOR EACH EPISODE PROVIDE:
EPISODE NUMBER
TITLE
ONE-SENTENCE PURPOSE
PRIMARY LOCATION
TIME WINDOW
CHARACTERS PRESENT
DOMINANT PROP
EMOTIONAL STATE AT START
EMOTIONAL STATE AT END
CENTRAL QUESTION
ONE MAJOR DRAMATIC EVENT
ONE IMPORTANT NEW PIECE OF INFORMATION
ONE EMOTIONAL TURN
FINAL IMAGE
UNANSWERED NEXT-EPISODE QUESTION

EPISODE RULE:
Each episode is ONE dramatic scene made from three 10-second video-generation micro-
sequences.

Each 10-second micro-sequence may contain multiple cinematic shots.
The shots must be motivated by story information or emotional reaction.

Do not force a one-shot camera take.
Do not create visual filler.
Do not use arbitrary camera movement.
Do not introduce unrelated locations merely to create variety.

SHORT-FORM RULE:
The first second must communicate something worth discovering.
The viewer should understand who matters by approximately the first five seconds.
The situation should change before the ten-second mark.
The episode should end with one answer and one stronger question.

Return only the canonical series blueprint.
```

---

# 9. CHARACTER REFERENCE PROMPT

```text
Create the CANONICAL CHARACTER REFERENCE for an original live-action Western drama
character.

CHARACTER NAME:
{NAME}

AGE:
{AGE}

ROLE:
{ROLE}

PERSONALITY:
{PERSONALITY}

FACE:
{EXACT_FACE_DESCRIPTION}

HAIR:
{HAIR}

FACIAL HAIR:
{FACIAL_HAIR}

EYES:
{EYES}

BODY:
{BODY}

DISTINCTIVE FEATURES:
{DISTINCTIVE_FEATURES}

WARDROBE:
{WARDROBE}

HAT:
{HAT}

BOOTS:
{BOOTS}

SIGNATURE PROP:
{PROP}

PERIOD:
{PERIOD}

Create a clean vertical 9:16 photorealistic live-action character reference sheet.

Show EXACTLY THE SAME PERSON in four views:

1. front full-body neutral pose;
2. 3/4 full-body view;
3. side profile portrait;
4. natural action pose.

IDENTITY LOCK:
Preserve exact facial proportions, eye shape, nose, jawline, cheekbones, hairline,
facial hair, age, skin characteristics and body proportions.

WARDROBE LOCK:
Preserve exact coat, shirt, vest, trousers, belt, boots, hat, jewelry and signature
prop.

REALISM:
Photorealistic live-action actor.
Natural skin pores.
Natural hair strands.
Real cotton, wool, leather and metal.
Physically believable Western costume.

CAMERA:
85mm portrait language.
Eye-level.
Natural perspective.
No fisheye.
No extreme distortion.

LIGHTING:
Soft neutral studio light.
Subtle key.
Gentle fill.
Natural skin rendering.

BACKGROUND:
Plain neutral studio background.
No scenery.
No other characters.

DO NOT:
change age,
change face,
change hair,
change wardrobe,
add modern objects,
add text,
add labels,
add logos,
add another person,
create duplicate limbs,
create fantasy styling,
create cartoon anatomy.

This is the canonical identity reference and must be reused throughout the series.
```

---

# 10. CHARACTER EXPRESSION / PERFORMANCE REFERENCE PROMPT

```text
Using the supplied CANONICAL CHARACTER REFERENCE, create a performance reference for the
SAME PERSON.

Preserve exact identity, age, hairstyle, facial hair, body proportions, wardrobe and
accessories.

Create six subtle live-action performance states:

1. guarded
2. hopeful
3. worried
4. shocked
5. quietly heartbroken
6. emotionally resolved

Use realistic micro-expression:

eye movement
breathing
jaw tension
small mouth changes
slight brow movement
gaze avoidance
posture
hand tension

Do not overact.
Do not turn every emotion into crying.

Photorealistic live-action.
85mm portrait language.
Neutral studio background.
Soft natural light.
Vertical 9:16.
No text.
No labels.
No identity drift.
```

---

# 11. LOCATION REFERENCE PROMPT

```text
Create the CANONICAL LOCATION REFERENCE for an original live-action Western drama.

LOCATION:
{LOCATION_NAME}

PERIOD:
{PERIOD}

PURPOSE:
{STORY_PURPOSE}

DESCRIPTION:
{DESCRIPTION}

Create one consistent vertical 9:16 environment reference.

LOCK:
architecture,
door positions,
window positions,
stairs,
porch,
fence,
trees,
terrain,
major furniture,
practical light sources,
surface materials,
weather state,
surrounding geography.

VISUAL WORLD:
physically believable frontier construction;
weathered wood,
iron,
leather,
cloth,
stone,
dust,
glass,
natural earth.

CAMERA:
50mm natural cinematic perspective.
Eye-level.
Realistic depth.

LIGHT:
Motivated natural or period-practical lighting.

Do not include modern infrastructure, vehicles, utility poles, contemporary signs,
plastic objects, modern furniture, logos or watermarks.

This is the canonical location reference.
```

---

# 12. PROP REFERENCE PROMPT

```text
Create the CANONICAL PROP REFERENCE for this story-critical object.

PROP:
{PROP}

MEANING:
{MEANING}

PERIOD:
{PERIOD}

MATERIAL:
{MATERIAL}

CONDITION:
{CONDITION}

Create a clean vertical reference showing:
front,
3/4,
side,
detail.

Preserve exact shape, dimensions, wear, scratches, color, damage, material and
orientation.

No modern manufacture cues.
No logos.
No watermark.

This prop must remain visually identical wherever it appears in later episodes.
```

---

# 13. VISUAL MOTIF PROMPT

```text
Create 3-5 recurring visual motifs for this Western emotional drama.

Each motif must have story meaning.

For each motif define:
MOTIF
FIRST APPEARANCE
INITIAL MEANING
MEANING AFTER THE REVERSAL
FINAL APPEARANCE
FINAL MEANING

Potential motifs:
letter,
photograph,
pocket watch,
empty chair,
horse,
saddle,
wedding ring,
lantern,
hat,
grave marker,
porch,
church bell,
train whistle.

Do not add motifs only for decoration.
A motif must gain or change meaning through the story.
```

---

# 14. THE CINEMATIC SHOT-DIRECTOR PROMPT

This stage happens **before** the final Google Flow prompt.

```text
You are the CINEMATOGRAPHER and EDITOR for a short-form Western drama.

Design the cinematic shot sequence for ONE 10-second micro-sequence.

INPUT:
STORY BEAT
CHARACTERS
LOCATION
EMOTIONAL STATE
PREVIOUS BLOCK END STATE
NEXT BLOCK PURPOSE

Return 2-5 short shots only when each shot has a clear story function.

For each shot define:

SHOT NUMBER
TIME RANGE
SHOT SIZE
CAMERA ANGLE
CAMERA HEIGHT
LENS LANGUAGE
CAMERA POSITION
CAMERA MOVEMENT
FOCUS BEHAVIOR
CHARACTER BLOCKING
FACIAL PERFORMANCE
IMPORTANT PROP
LIGHTING
COMPOSITION
DIALOGUE
DIEGETIC SOUND
SHOT PURPOSE
TRANSITION INTO NEXT SHOT

CINEMATIC PURPOSE OF SHOT SIZES:

EXTREME WIDE:
scale, isolation, geography.

WIDE:
character in environment.

MEDIUM-WIDE:
body language + location.

MEDIUM:
dialogue and interpersonal interaction.

MEDIUM CLOSE-UP:
strong reaction while preserving some environment.

CLOSE-UP:
emotional truth.

EXTREME CLOSE-UP:
story-critical eye, hand or object.

CAMERA ANGLES:

EYE LEVEL:
neutral intimacy.

SLIGHT LOW ANGLE:
power, resolve, threat.

SLIGHT HIGH ANGLE:
vulnerability, defeat, isolation.

OVER-THE-SHOULDER:
relationship tension and dialogue.

PROFILE:
separation, contemplation.

THREE-QUARTER:
preferred emotional portrait angle.

POV:
use only when the viewer must see exactly what the character sees.

LENS LANGUAGE:

24-28mm:
large environment and physical scale.

35mm:
immersive narrative space and movement.

50mm:
natural dialogue and character interaction.

65mm:
balanced character/environment isolation.

85mm:
intimate emotion.

100mm macro:
critical object or tiny detail.

CAMERA MOVEMENT:

SLOW PUSH-IN:
realization, intimacy, confession.

SLOW PULL-BACK:
isolation, loss.

LATERAL TRACK:
following movement, relationship progression.

SUBTLE ARC:
revelation or changing relationship.

LOCKED-OFF:
truth, grief, silence.

CONTROLLED HANDHELD:
panic or instability.

RACK FOCUS:
change of narrative attention.

RULE:
Do not repeat movements randomly.
Every movement needs narrative motivation.

EDITING RULE:
Shots may cut quickly, but each cut must have a reason:
new information,
new reaction,
new point of view,
or emotional emphasis.

Return a concise shot sequence, not a prose essay.
```

---

# 15. CAMERA GRAMMAR PRESETS

## Preset A - Information -> Reaction

```text
35mm medium
cut to
85mm close-up
```

Use when a piece of information immediately changes a character.

## Preset B - Question -> Answer

```text
50mm over-the-shoulder
cut to
50mm reverse over-the-shoulder
cut to
85mm reaction
```

Use for dialogue-driven confrontation.

## Preset C - Object -> Meaning

```text
100mm detail
cut to
85mm face
```

Use for letters, rings, photographs, watches or weapons with story significance.

## Preset D - Arrival -> Threat

```text
24-35mm wide
slow push
cut to
50mm medium
cut to
85mm reaction
```

Use when a character or threat enters the emotional space.

## Preset E - Quiet Grief

```text
50mm medium
locked off
cut to
85mm close-up
hold
```

Use when silence carries the scene.

## Preset F - Revelation

```text
35-50mm medium
subtle arc
rack focus to hidden detail
cut to
85mm reaction
```

Use when the audience discovers meaning at the same time as the character.

---

# 16. SCREEN GEOGRAPHY RULE

Even though the episode uses multiple cuts, the audience must never become spatially confused.

Lock the interaction axis.

If Character A is screen-left and Character B is screen-right in the master coverage, preserve that relationship unless a deliberate axis-crossing shot is necessary.

Avoid:

```text
A screen-left
B screen-right
CUT
A screen-right
B screen-left
```

unless the prompt explicitly communicates the physical transition.

Use:

```text
same eye-line
same room geography
same doorway direction
same walking direction
same prop hand
same relative character positions
```

---

# 17. CONTINUITY STATE MODEL

For every 10-second micro-sequence, preserve:

```text
CHARACTER STATE
LOCATION STATE
PROP STATE
LIGHT STATE
WEATHER STATE
EMOTIONAL STATE
SCREEN DIRECTION
CAMERA STATE
```

Store three transition checkpoints:

```text
B0 = beginning of 30-second episode
B1 = end of generation 01
B2 = end of generation 02
B3 = end of generation 03
```

Unlike the previous version, B1/B2/B3 are not necessarily single camera frames.
They are **continuity states** describing what must be true when the next generation begins.

When Flow start/end frames are available, use generated anchors to make those continuity states visually explicit.

---

# 18. MASTER 10-SECOND GOOGLE FLOW MICRO-SEQUENCE PROMPT

This is the primary generation template.

```text
Create a 10-second vertical 9:16 live-action cinematic Western drama micro-sequence.

THIS IS ONE CONTINUOUS DRAMATIC BEAT, NOT A RANDOM MONTAGE.

Use the supplied character references, location references and prop references as
canonical visual sources.

EPISODE:
{EPISODE}

MICRO-SEQUENCE:
{01 / 02 / 03}

STORY PURPOSE:
{WHAT CHANGES DURING THESE 10 SECONDS}

START STATE:
{PREVIOUS END STATE}

END STATE:
{NEXT STATE}

CHARACTER REFERENCES:
{REFERENCES}

LOCATION REFERENCE:
{LOCATION}

PROP REFERENCE:
{PROP}

VISUAL STYLE:
Photorealistic live-action Western feature-film aesthetic.
Authentic frontier setting.
Natural skin texture.
Real fabric, leather, wood and metal.
Natural atmospheric depth.
Restrained cinematic contrast.
Natural highlight rolloff.

EDITING STRUCTURE:

SHOT 01 - {TIME}
{SHOT DESCRIPTION}
Camera: {SIZE + ANGLE + HEIGHT + LENS}
Movement: {MOVEMENT}
Focus: {FOCUS}

SHOT 02 - {TIME}
{SHOT DESCRIPTION}
Camera: {SIZE + ANGLE + HEIGHT + LENS}
Movement: {MOVEMENT}
Focus: {FOCUS}

SHOT 03 - {TIME}
{SHOT DESCRIPTION}
Camera: {SIZE + ANGLE + HEIGHT + LENS}
Movement: {MOVEMENT}
Focus: {FOCUS}

Add another shot only if it is essential to the dramatic beat.

CHARACTER PERFORMANCE:
Use subtle, realistic micro-expression.
Communicate emotion through eyes, breathing, posture, hands, gaze and hesitation.
Avoid theatrical overacting.

BLOCKING:
{EXACT PHYSICAL ACTION}

DIALOGUE:
{EXACT DIALOGUE OR NONE}

LIGHTING:
{MOTIVATED LIGHT SOURCE + DIRECTION + QUALITY}

ATMOSPHERE:
{WIND + DUST + WEATHER + CLOTHING + ENVIRONMENTAL MOTION}

AUDIO:
{DIEGETIC SOUND + DIALOGUE + IMPORTANT SFX + MUSIC IF NEEDED}

EDITING:
Use clean motivated cinematic cuts.
The sequence must feel like one coherent scene photographed by the same cinematographer.
Do not create unrelated compositions.
Do not introduce a new location unless explicitly required.

CONTINUITY:
Preserve exact character identity, wardrobe, age, hairstyle, facial hair, body
proportions, location geometry, prop identity, lighting direction, time window, weather
and screen geography.

FINAL FRAME / END STATE:
{EXACT FINAL VISUAL STATE}

QUALITY GUARD:
No identity drift.
No wardrobe drift.
No age change.
No random character.
No random prop.
No location redesign.
No modern objects.
No time-of-day jump.
No lighting-direction jump.
No screen-direction reversal.
No face morphing.
No malformed hands.
No duplicated limbs.
No impossible horse movement.
No text.
No logos.
No watermark.
No embedded subtitles.

The result should look like real footage from a high-end Western feature film edited
into a short-form emotional scene.
```

---

# 19. MICRO-SEQUENCE 01 PROMPT SPECIALIZATION - HOOK

```text
Purpose:
HOOK + CHARACTER + QUESTION

The first frame must already contain narrative information.

Do not begin with an empty landscape.
Do not begin with generic cowboy walking.
Do not waste the opening on an unmotivated establishing shot.

Preferred pattern:

SHOT 01:
visual hook or unusual action.

SHOT 02:
medium character shot or dialogue.

SHOT 03:
close reaction or story clue.

ENDING:
leave one clear question unanswered.
```

---

# 20. MICRO-SEQUENCE 02 PROMPT SPECIALIZATION - PRESSURE

```text
Purpose:
NEW INFORMATION + ESCALATION + REACTION

Begin from the exact narrative state created by Micro-Sequence 01.

Preferred pattern:

SHOT 01:
continuation or immediate reaction.

SHOT 02:
over-the-shoulder, medium or medium close-up for new information.

SHOT 03:
close-up reaction.

OPTIONAL SHOT 04:
important prop or environmental reveal.

The situation must be different by the end of the 10 seconds.

The audience should now understand what the character could lose.
```

---

# 21. MICRO-SEQUENCE 03 PROMPT SPECIALIZATION - PAYOFF + CLIFFHANGER

```text
Purpose:
CONSEQUENCE + EMOTIONAL TURN + NEXT QUESTION

Preferred pattern:

SHOT 01:
immediate consequence.

SHOT 02:
intimate reaction.

SHOT 03:
story-critical reveal or object detail.

SHOT 04:
final face / final visual.

The last 2 seconds should become visually simple.

Use a strong final composition:
face,
object,
doorway,
distant figure,
empty space,
horse reaction,
letter,
photograph,
gravestone,
or another story-critical visual.

The final image must:

answer one small question
AND
create one larger question.

No arbitrary shock.
No unrelated new villain.
No random explosion.
No random attack.
No random accident.

The next episode must feel necessary because the viewer cares what happens next.
```

---

# 22. DIALOGUE PROMPT

```text
Write only the dialogue required for this exact 30-second Western drama episode.

RULES:

1. Dialogue must sound spoken.
2. Use short sentences.
3. Avoid exposition.
4. Never explain what the audience can already see.
5. Each line must reveal character, increase pressure, alter the relationship, or create
a question.
6. Silence is allowed.
7. Avoid speeches.
8. Keep spoken material short enough for natural performance.
9. The scene must remain understandable if the dialogue is muted.
10. Do not invent facts that contradict the canonical story.

Format:
CHARACTER - DELIVERY - LINE

Examples of delivery:
quiet and guarded
low and controlled
hesitating
voice barely above a whisper
disbelieving
trying not to cry
angry but restrained
```

---

# 23. EMOTIONAL PERFORMANCE PROMPT

```text
Direct the actors like a serious live-action feature film.

Do not overact.

Emotion should appear through:

eyes
breathing
posture
hands
gaze
hesitation
jaw tension
shoulders
movement speed
micro-expression

GRIEF:
restraint, delayed reaction, controlled breathing, eyes avoiding contact.

FEAR:
frozen posture, scanning eyes, shallow breathing, hesitation.

LOVE:
softened gaze, relaxed shoulders, careful physical distance.

GUILT:
averted gaze, jaw tension, delayed response, still hands.

HOPE:
slight lift of posture, softened eyes, restrained smile.

BETRAYAL:
brief disbelief, then emotional withdrawal or controlled anger.

Make the emotion internal and observable, not theatrical.
```

---

# 24. LIGHTING + ATMOSPHERE PROMPT

```text
Use physically motivated period-appropriate lighting.

DAY:
natural sunlight,
realistic bounce,
dust-filled atmosphere,
long or short shadows according to time of day.

INTERIOR:
window light,
oil lamp,
candle,
firelight.

NIGHT:
moonlight or period practicals,
readable deep shadows.

EMOTIONAL LIGHTING:

grief:
soft directional light, gentle negative fill.

hope:
warm motivated light and open face.

danger:
higher contrast and deeper shadow.

revelation:
use contrast and focus to draw attention to the story-critical face or object.

Do not use modern LED-looking colored lighting unless the story explicitly requires it.

Atmosphere must remain physically believable:
wind affects dust,
wind affects hair,
wind affects cloth,
wood creaks,
fire flickers,
horses react naturally.
```

---

# 25. REFERENCE-DRIVEN FLOW PROMPT

Google Flow supports adding characters and visual references/ingredients to help maintain consistency across clips. The prompt should explicitly tell Flow what each reference represents and must not contradict the input images. [Section 26]

```text
Use these supplied images as CANONICAL REFERENCES.

REFERENCE A:
{CHARACTER A}

REFERENCE B:
{CHARACTER B}

REFERENCE C:
{LOCATION}

REFERENCE D:
{PROP}

Treat these images as identity references, not loose inspiration.

Preserve exact character face, age, hairstyle, facial hair, body proportions and
wardrobe.
Preserve location architecture and recognizable geometry.
Preserve the prop shape, wear and materials.

Use the references consistently throughout this 10-second cinematic micro-sequence.

Do not redesign, merge or reinterpret the references.
```

---

# 26. CURRENT GOOGLE FLOW FACTS TO RESPECT

As of the current Google Flow documentation checked during this audit:

- Gemini Omni Flash 1.1 supports Text to Video.
- Gemini Omni Flash 1.1 supports First Frame video generation.
- Gemini Omni Flash 1.1 supports First + Last Frames.
- Gemini Omni Flash 1.1 supports Ingredients/References to Video.
- Gemini Omni Flash 1.1 supports video-to-video editing up to 10 seconds.
- Gemini Omni Flash 1.1 supports 4s, 6s, 8s and 10s generations for the listed video modes.
- Flow documents start/end frames as a way to create transitions or animate a defined visual state.
- Flow documents ingredients as a way to reuse characters and key objects across clips.
- Flow documents voice references for Omni Flash generations when ingredients are used.
- Google recommends clean reference images and warns that prompt text should complement rather than contradict supplied visual inputs.

Google currently lists Omni 360p as a lower-cost generation option, with 720p standard output also available depending on plan/settings. Exact credit costs should be checked in the active Flow interface before large batches.

Sources:

1. Google Flow Help - Learn about Flow models and supported features
https://support.google.com/flow/answer/16352836

2. Google Flow Help - Create videos in Google Flow
https://support.google.com/flow/answer/16353334

3. Google Flow Help - Edit videos and build scenes in Google Flow
https://support.google.com/flow/answer/16935718

4. Google Flow Agent Help
https://support.google.com/labs/answer/17093911

---

# 27. PROMPT PRECEDENCE CONTRACT

Long prompts can conflict with themselves.

Use this priority order:

```text
1. STORY TRUTH
2. CANONICAL CHARACTER / LOCATION / PROP REFERENCES
3. CONTINUITY FROM PREVIOUS BLOCK
4. CHARACTER ACTION / BLOCKING
5. EDITING STRUCTURE
6. CAMERA / LENS / MOVEMENT
7. LIGHTING
8. ATMOSPHERE
9. AUDIO
10. STYLE POLISH
```

If a lower-priority instruction conflicts with a higher-priority rule, preserve the higher-priority rule.

---

# 28. ACTION BUDGET

A 10-second micro-sequence should generally contain:

```text
1 major dramatic action
+
1 major reaction
+
1 important visual detail
+
2-5 motivated shots
```

Do not overload one generation with many unrelated physical actions.

GOOD:

```text
woman opens letter
-> reads line
-> reacts
-> sees chapel
```

TOO MUCH:

```text
woman rides in
-> dismounts
-> runs upstairs
-> opens door
-> fights man
-> drops gun
-> hugs child
-> horse runs away
-> rain starts
```

---

# 29. SHOT BUDGET

Default:

```text
10 seconds = 2-5 shots
```

Suggested distributions:

### Dialogue beat

```text
2-3 shots
```

### Reveal beat

```text
3-4 shots
```

### High-emotion beat

```text
2-4 shots
```

### Action beat

```text
3-5 shots
```

Do not cut merely for variety.

If one uninterrupted shot is more powerful, use one shot.

If a reaction needs a close-up, cut to the close-up.

---

# 30. EDITING GRAMMAR PROMPT

```text
Act as a professional short-form drama editor.

Given the supplied 10-second micro-sequence, determine the cut points based on STORY
INFORMATION.

Cut when:

- a new character becomes important;
- a new fact is revealed;
- the listener needs a reaction shot;
- the audience must see a story-critical object;
- the emotional point of view changes;
- physical geography needs clarification.

Avoid cuts when:

- nothing has changed;
- the cut exists only for spectacle;
- it destroys emotional tension;
- it creates spatial confusion;
- it resets the character's physical continuity.

The editing style should feel like a polished live-action drama scene, not a slideshow
of AI-generated images.
```

---

# 31. HOOK GENERATOR PROMPT

```text
Generate 12 original opening concepts for this Western drama episode.

Each must work visually in the FIRST SECOND.

Possible hook mechanisms:

an unusual human action
an emotionally loaded object
a surprising relationship
an obvious consequence
an unanswered discovery
a character arriving unexpectedly
a secret being overheard
a promise being broken
a person appearing where they should not be

Avoid generic:
cowboy walking
horse running
sunset
empty town
random gunfight
landscape only

For each provide:
HOOK IMAGE
IMMEDIATE QUESTION
WHY IT CONNECTS TO THE MAIN STORY

Then select a hook that communicates the most story with the least exposition.
```

---

# 32. CLIFFHANGER GENERATOR PROMPT

```text
Generate 10 possible ending images for this 30-second Western drama episode.

Each ending must:

1. emerge directly from the existing scene;
2. answer one immediate question;
3. create a more important unanswered question;
4. involve an established character, relationship, prop, promise or secret;
5. remain visually clear in one frame.

Avoid random explosions, attacks, accidents or unrelated new characters.

The next episode must feel necessary because the viewer cares what happens to an
established human relationship or mystery.
```

---

# 33. CONTINUITY GUARD PROMPT

Run this before releasing every generation prompt.

```text
You are the CONTINUITY SUPERVISOR.

Compare the previous generation against the proposed next generation.

VERIFY:

CHARACTER
same face?
same age?
same hair?
same facial hair?
same body proportions?
same wardrobe?
same hat?
same boots?

LOCATION
same architecture?
same room orientation?
same doors and windows?
same terrain?
same weather?

PROP
same shape?
same condition?
same hand?
same position?

LIGHT
same time window?
same light direction?
same shadow logic?

SCREEN GEOGRAPHY
same left/right relationship?
same eye-line?
same walking direction?
same 180-degree axis?

EMOTION
does the new performance logically follow the previous emotional state?

CAMERA
does the composition continue naturally?
does the lens language make sense?
is the new angle motivated?

STORY
does the scene introduce anything not present in the canonical episode?

If any answer is NO:
REWRITE THE NEXT VIDEO PROMPT.
Do not change the canonical story to solve continuity.
```

---

# 34. VIDEO PROMPT AUDITOR

```text
Audit this 10-second Google Flow video prompt for production readiness.

STORY:
Does every shot advance the story?
Is there one clear dramatic beat?

CHARACTER:
Is canonical identity referenced?
Is the performance observable and realistic?

EDITING:
Are cuts motivated?
Is the shot count reasonable?
Does the sequence remain one coherent scene?

CAMERA:
Is shot size specified?
Is angle specified?
Is camera height specified when useful?
Is lens language specified?
Is movement specified?
Is movement motivated?

COMPOSITION:
Is the subject clear in 9:16?
Is the emotional focal point readable?

LIGHT:
Is the source motivated?
Is continuity clear?

PHYSICS:
Are body movement, clothing, hair, props and horses physically believable?

AUDIO:
Is dialogue exact?
Are critical sound cues identified?

CONTINUITY:
Does the first shot naturally follow the previous block?
Does the final frame prepare the next block?

PROMPT CONFLICT:
Are instructions contradictory?

If the prompt is weak, rewrite it.
Return either:
PASS
or
REVISED PROMPT
```

---

# 35. CHARACTER VOICE PROMPT

When using Flow's voice-reference workflow:

```text
Create a stable character voice identity for:
{CHARACTER}

VOICE AGE:
{AGE}

VOICE QUALITY:
{QUALITY}

ACCENT:
{ACCENT}

DELIVERY:
{DELIVERY}

EMOTIONAL BASELINE:
restrained, intimate, naturalistic live-action dialogue.

Do not sound like a narrator.
Do not sound like a commercial voice-over.
Do not over-enunciate.
Do not imitate a known actor.

The voice should remain recognizable across episodes.
```

Google documents voice references for Omni Flash when ingredients are used. Availability can vary by region and feature configuration. [Google Flow Help, Section 26]

---

# 36. VOICE + DIALOGUE CONTINUITY

The same character should maintain:

```text
voice identity
accent
age impression
pace
vocal texture
emotional baseline
```

Do not change a character's voice merely because the episode changes.

When dialogue is generated inside Flow, supply the voice reference when available.

When dialogue is generated separately, the same canonical voice profile must be used.

---

# 37. PERIOD-CORRECTNESS PROMPT

```text
Maintain strict visual consistency with the chosen Western period:
{YEAR / DECADE}

Reject accidental modern details.

Check:
clothing
hair
architecture
transportation
weapons
tools
furniture
lighting
signage
materials

Do not introduce modern plastics, contemporary utility infrastructure, modern vehicles,
electric streetlights, synthetic-looking materials or current fashion.
```

---

# 38. FINAL 30-SECOND EPISODE MASTER GENERATOR

This is the Hermes orchestration prompt.

```text
You are the FINAL WESTERN DRAMA PROMPT DIRECTOR.

INPUTS:
SERIES BIBLE
CHARACTER BIBLE
LOCATION BIBLE
PROP BIBLE
EPISODE BLUEPRINT
PREVIOUS EPISODE END STATE
CURRENT EPISODE PURPOSE

TASK:
Create the complete prompt package for ONE 30-second Western emotional drama episode.

PRODUCTION:
3 x 10-second Gemini Omni Flash 1.1 video generations.
Vertical 9:16.

IMPORTANT:
Each 10-second generation is a CINEMATIC MICRO-SEQUENCE.
It may contain multiple motivated shots.

Do NOT treat the three generations as unrelated videos.
They are consecutive dramatic beats within one scene.

FOR THE EPISODE CREATE:

1. CHARACTER REFERENCE PROMPTS
2. LOCATION REFERENCE PROMPTS
3. PROP REFERENCE PROMPTS
4. EPISODE STORY BLUEPRINT
5. CAMERA / SHOT BLUEPRINT
6. GENERATION 01 PROMPT
7. GENERATION 02 PROMPT
8. GENERATION 03 PROMPT
9. CONTINUITY PROMPT
10. FINAL AUDIT PROMPT

GENERATION 01:
Hook, character, question.

GENERATION 02:
Pressure, new information, reaction.

GENERATION 03:
Consequence, emotional turn, final reveal, cliffhanger.

SHOT DESIGN:
Each generation may contain approximately 2-5 motivated shots.

CAMERA REQUIREMENT:
Every shot must specify, when applicable:
shot size,
angle,
height,
lens,
position,
movement,
focus,
composition.

CAMERA MOTIVATION:
Push in for realization/intimacy.
Pull back for isolation.
Tracking for movement/pursuit.
Arc for revelation.
Locked off for truth/grief.
Controlled handheld for instability.
Rack focus for narrative attention shift.

STORY REQUIREMENT:
One dramatic event.
No filler.
No arbitrary spectacle.
No unrelated location.

IDENTITY REQUIREMENT:
Use canonical references whenever available.
Never redesign recurring characters.

CONTINUITY REQUIREMENT:
Preserve wardrobe, identity, location, prop, lighting, weather, time window, screen
geography and emotional state.

SHORT-FORM REQUIREMENT:
The first second must contain a story hook.
Every generation must change the dramatic state.
The final generation must leave a specific next-episode question.

PROMPT WRITING REQUIREMENT:
Use concrete observable instructions.
Convert vague words such as "cinematic", "emotional" and "dramatic" into camera,
movement, performance, lighting, composition and timing details.

OUTPUT RULE:
Return ONLY the requested prompt package.
No production essay.
No code.
No filler explanation.
```

---

# 39. COMPLETE EPISODE STORYFLOW TEMPLATE

Use this structure for every generated episode.

```text
EPISODE:
{NUMBER}

TITLE:
{TITLE}

PURPOSE:
{ONE SENTENCE}

LOCATION:
{LOCATION}

TIME WINDOW:
{TIME}

PRIMARY CHARACTERS:
{CHARACTERS}

DOMINANT PROP:
{PROP}

EMOTIONAL START:
{EMOTION}

EMOTIONAL END:
{EMOTION}

CENTRAL QUESTION:
{QUESTION}

MAJOR EVENT:
{EVENT}

NEW INFORMATION:
{INFORMATION}

REVERSAL / TURN:
{TURN}

FINAL IMAGE:
{IMAGE}

NEXT QUESTION:
{QUESTION}
```

---

# 40. COMPLETE SHOT BLUEPRINT TEMPLATE

```text
GENERATION:
{01 / 02 / 03}

STORY BEAT:
{BEAT}

SHOT 01:
TIME:
SIZE:
ANGLE:
HEIGHT:
LENS:
POSITION:
MOVEMENT:
FOCUS:
ACTION:
PERFORMANCE:
LIGHT:
DIALOGUE:
PURPOSE:

SHOT 02:
...

SHOT 03:
...

END STATE:
{STATE}
```

---

# 41. REPLAY / LOOP DESIGN

Use only when naturally supported by the story.

The final image can echo an earlier visual motif while changing its meaning.

Example:

```text
EPISODE OPEN:
father holds a sealed letter.

EPISODE END:
daughter holds the same letter.
```

The second viewing can cause the viewer to reinterpret the opening.

Do not force a loop where it damages the narrative.

---

# 42. AUDIO DESIGN PROMPT

```text
Design the sound concept for this 30-second Western emotional drama.

Prioritize:

1. dialogue
2. story-critical sound effects
3. environmental ambience
4. music

Possible diegetic sounds:
wind
boots on wood
boots on dirt
leather creaking
horse breathing
horse tack
wagon wheels
door hinges
oil lamp
fire
church bell
train whistle
rain on wood
distant town ambience

Use silence strategically.

Do not place music underneath every second.

When dialogue is important, preserve space around it.
```

---

# 43. FINAL PROMPT PACKAGING CONTRACT

The prompt-only output for one episode should look like:

```text
episodes/
  ep01/
    00_story_blueprint.txt
    01_character_reference_prompts.txt
    02_location_reference_prompts.txt
    03_prop_reference_prompts.txt
    04_camera_shot_blueprint.txt
    05_generation_01_flow_prompt.txt
    06_generation_02_flow_prompt.txt
    07_generation_03_flow_prompt.txt
    08_continuity_guard.txt
    09_final_audit.txt
```

The pipeline may also create:

```text
series_master_prompt.txt
visual_style_anchor.txt
character_voice_profiles.txt
```

No storyboard collage is required.

No CSV is required for the creative prompt layer.

---

# 44. HERMES SKILL WRAPPER CONTRACT

The final Hermes skill should be a compact entry point that invokes this detailed reference document.

Recommended structure:

```text
hermes-skills/
  media/
    western-emotional-drama/
      SKILL.md
      WESTERN_EMOTIONAL_DRAMA_PROMPT_PIPELINE_AUDITED_V2.md
```

The wrapper should:

1. activate for requests involving original cinematic Western drama prompts;
2. load the detailed pipeline reference;
3. preserve the 30-second / 3-generation contract;
4. prioritize prompt generation over general writing;
5. enforce reference-driven character consistency;
6. enforce the cinematic shot grammar;
7. return copy-paste-ready Flow prompts.

---

# 45. RECOMMENDED HERMES WRAPPER SKILL

```yaml
---
name: western-emotional-drama
description: "Create prompt-only production packages for original serialized cinematic
Western emotional dramas. Use for character references, locations, props, storyflow,
cinematography, shot design, and exactly three 10-second Google Flow Gemini Omni Flash
1.1 video prompts per 30-second episode."
version: 2.1.0
---

# Western Emotional Drama

Use this skill when the user wants an original serialized Western emotional drama
generated as cinematic AI-video prompts.

## Core Contract

- Prompt-only output.
- 30 seconds per episode.
- Exactly 3 video generations per episode.
- Each generation is 10 seconds.
- Each generation is a cinematic micro-sequence and may contain multiple motivated
shots.
- The three generations must form one coherent dramatic scene.
- Character and location references are canonical.
- Camera language must be explicit and story-motivated.
- The ending must create a specific next-episode question.

## Workflow

1. Load the detailed pipeline document.
2. Build or update the canonical series bible.
3. Build character, location and prop reference prompts.
4. Define the episode's emotional event.
5. Build the shot blueprint.
6. Generate exactly three 10-second Flow prompts.
7. Run continuity guard.
8. Run final prompt audit.
9. Return only the requested prompt artifacts.

## Style

Photorealistic live-action Western drama.
Prestige-film cinematography.
Naturalistic acting.
Motivated camera movement.
Purposeful cuts.
Strong close-up reactions.
Period-authentic production design.

## Camera Requirement

Every cinematic prompt should specify the shot size, angle, lens language, movement,
focus and blocking when those details affect the shot.

Never add camera movement purely because it sounds cinematic.

## Continuity Requirement

Preserve:
character identity;
wardrobe;
location;
props;
time window;
lighting;
weather;
screen geography;
emotional state.

## Story Requirement

One episode = one dramatic event.
One event = one emotional change.
One ending = one new question.

Read:
`WESTERN_EMOTIONAL_DRAMA_PROMPT_PIPELINE_AUDITED_V2.md`
for the complete production prompt system.
```

---

# 46. FINAL QUALITY CHECKLIST

Before a prompt package is released, verify:

## STORY

```text
[ ] Original premise
[ ] Clear emotional question
[ ] One dramatic event
[ ] No filler
[ ] Meaningful change
[ ] Strong ending question
```

## CHARACTER

```text
[ ] Canonical identity reference
[ ] Consistent age
[ ] Consistent face
[ ] Consistent wardrobe
[ ] Consistent voice profile
[ ] Emotion shown through behavior
```

## CINEMATOGRAPHY

```text
[ ] Shot sizes are intentional
[ ] Angles are intentional
[ ] Lens choices support emotion
[ ] Camera movement has a reason
[ ] Focus changes have a reason
[ ] Composition is readable in 9:16
[ ] Screen geography is consistent
```

## GENERATION

```text
[ ] Exactly 3 generations
[ ] Exactly 10 seconds each
[ ] Each is a coherent micro-sequence
[ ] Cuts are motivated
[ ] No random montage
[ ] No excessive actions
```

## CONTINUITY

```text
[ ] Character continuity
[ ] Location continuity
[ ] Prop continuity
[ ] Light continuity
[ ] Weather continuity
[ ] Emotional continuity
```

## FLOW COMPATIBILITY

```text
[ ] References named clearly
[ ] Prompt does not contradict references
[ ] Start/end frames used when useful and available
[ ] Ingredients used when useful and available
[ ] Voice reference used when required and available
```

## FINAL IMPACT

```text
[ ] First second has a hook
[ ] Viewer understands who matters quickly
[ ] Something changes before 10 seconds
[ ] Middle introduces meaningful pressure
[ ] Final image is memorable
[ ] Next episode has a specific reason to exist
```

---

# 47. FINAL CREATIVE FORMULA

The definitive production formula is:

```text
ORIGINAL STORY
      |
      v
CHARACTER BIBLE
      |
      v
LOCATION / PROP BIBLE
      |
      v
EPISODE EMOTIONAL EVENT
      |
      v
CINEMATIC SHOT BLUEPRINT
      |
      +-----------------------------+
      |                             |
      v                             v
10s MICRO-SEQUENCE 01        CONTINUITY STATE B1
HOOK + QUESTION                     |
      |                             |
      v                             v
10s MICRO-SEQUENCE 02        CONTINUITY STATE B2
PRESSURE + REACTION                 |
      |                             |
      v                             v
10s MICRO-SEQUENCE 03        FINAL STATE B3
PAYOFF + CLIFFHANGER                |
      |                             |
      +---------------+-------------+
                      v
                 30-SECOND
                 EPISODE
                      |
                      v
              NEXT QUESTION
                      |
                      v
                NEXT EPISODE
```

### Final locked rules

```text
30s EPISODE
= 3 x 10s GENERATIONS

10s GENERATION
= CINEMATIC MICRO-SEQUENCE
= 2-5 MOTIVATED SHOTS WHEN NEEDED

EVERY SHOT
= STORY INFORMATION OR EMOTIONAL PURPOSE

EVERY CAMERA MOVE
= NARRATIVE MOTIVATION

EVERY CUT
= NEW INFORMATION OR REACTION

EVERY CHARACTER
= CANONICAL REFERENCE

EVERY EPISODE
= ONE DRAMATIC EVENT

EVERY EPISODE END
= ONE ANSWER + ONE NEW QUESTION

ENTIRE SERIES
= ONE EMOTIONAL ARC WITHOUT FILLER
```

---

# 48. SOURCES

Google Flow model capabilities and current feature support: 
[Google Flow Help - models and supported features](https://support.google.com/flow/answer/16352836)

Google Flow video creation, frames, ingredients, references and voice references:  
[Google Flow Help - create videos](https://support.google.com/flow/answer/16353334)

Google Flow video editing and scene tools:  
[Google Flow Help - edit videos and build scenes](https://support.google.com/flow/answer/16935718)

Google Flow Agent instructions and workflow:  
[Google Labs Help - Flow Agent](https://support.google.com/labs/answer/17093911)

Reference animation pipeline supplied by the user:  
[Koyawel animation pipeline](https://github.com/koyawel0694/animation-pipeline-koyawel)

Reference Hermes media skill:  
[Koyawel Hermes media SKILL.md](https://raw.githubusercontent.com/koyawel0694/animation-pipeline-koyawel/main/hermes-skills/media/animation-pipeline-koyawel/SKILL.md)

Reference character policy:  
[Koyawel character reference policy](https://raw.githubusercontent.com/koyawel0694/animation-pipeline-koyawel/main/character_reference_policy.md)

Reference Flow prompt exporter:  
[Koyawel Flow prompt exporter](https://raw.githubusercontent.com/koyawel0694/animation-pipeline-koyawel/main/build_block_prompts_txt.py)

---

# 49. FINAL PRINCIPLE

The objective is not:

```text
three attractive AI clips
```

It is:

```text
one emotionally coherent 30-second drama
```

built from:

```text
one canonical story
one consistent cast
one coherent world
purposeful shot design
motivated camera language
natural performances
strong visual information
and a specific unanswered question
```

The system should make the audience think:

> **"Wait... what happens next?"**

That is the reason the next episode exists.
