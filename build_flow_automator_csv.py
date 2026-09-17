#!/usr/bin/env python3
"""
build_flow_automator_csv.py — Construct Google Flow Automator Max V3 production CSVs in 100% ENGLISH.

Follows the canonical SERYE / Flow Automator Max schema:
  prompt,description,hashtags,videoModel,videoMode,videoDurationSeconds,flowQuantity,videoVoiceReference,flowAspectRatio

Features:
- 100% English dialogue and voice acting scripts
- Character @mentions prepended for automatic Flow React Fiber asset binding (@Kang Jin-Hoo, etc.)
- 11-Part Masterclass prompt architecture (Subject, Action, Camera, Lens, Lighting, Style, Emotion, VO, SFX)
- Exact 10-second block timing with 0s-10s duration
- Explicit held freeze frame on final beat of every block
- Generates:
  1. e01.csv (all 6 blocks for Episode 1)
  2. block1_queue.csv .. block6_queue.csv (individual queue files)
  3. block1_video_prompt.txt .. block6_video_prompt.txt (raw prompt text)
  4. char_refs_investor.csv (character reference sheet generation queue)
"""

import csv
import json
import os
import sys
from pathlib import Path

SERIES = "investor_who_sees_the_future"
SERIES_TITLE = "The Investor Who Sees The Future"
HASHTAGS = "#manhwa #investor #kdrama #drama #shortDrama #googleFlow #webtoon"
MODEL = "Omni Flash"
MODE = "ingredients"
DURATION = "10"
QUANTITY = "1"
ASPECT = "9:16"

CSV_HEADER = [
    "prompt",
    "description",
    "hashtags",
    "videoModel",
    "videoMode",
    "videoDurationSeconds",
    "flowQuantity",
    "videoVoiceReference",
    "flowAspectRatio",
]

BLOCKS_DATA = [
    {
        "block_num": 1,
        "title": "The Question That Changes Everything",
        "cast_mentions": ["@Street Reporter", "@Shin Yuri"],
        "description": f"VIDEO: E01 B1 — The Question That Changes Everything",
        "voice_ref": "English broadcast male and witty female",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE OPENING",
                "content": "wide establishing crane shot descending into a bustling modern metropolitan pedestrian shopping plaza; STREET REPORTER (young Korean male in early 20s, tailored charcoal-gray suit, white collared dress shirt, slim black tie, holding matte-black handheld microphone with blue windscreen) stands in center frame; camera operator in black cap films him in foreground; daylight 5600K ambient city reflections",
                "camera": "crane down from high angle into medium wide tracking, 24mm equivalent lens",
                "emotion": "energetic, bright professional television broadcast smile, engaging eye contact with lens",
                "vo": '(Street Reporter): "(energetic, crisp broadcast projection) Have you ever wondered what you would do if a fortune landed in your hands overnight?"',
                "sfx": "bustling urban street ambience, footsteps on cobblestones, faint traffic hum",
            },
            {
                "time": "1.5s-3s",
                "label": "THE TURN",
                "content": "reporter lunges forward enthusiastically toward passersby, extending microphone with an inquisitive smile; background shoppers in modern casual streetwear stop and glance over curiously",
                "camera": "smooth dynamic low-angle push-in toward reporter\'s microphone, 35mm lens",
                "emotion": "sharp, curious, theatrical broadcast inflection, eyebrows raised in challenge",
                "vo": '(Street Reporter): "(dramatic, teasing, eyes wide) What if you suddenly received one hundred million won in cold hard cash?!"',
                "sfx": "sharp mic movement swoosh, crowd murmur react",
            },
            {
                "time": "3s-4.5s",
                "label": "THE REACTION",
                "content": "cinematic medium shot of SHIN YURI (young Korean woman, wavy honey-blonde hair, beige button-up blouse, delicate gold necklace) walking down the sidewalk; she pauses, rests one manicured finger on her chin, and smiles warmly with effortless intelligence",
                "camera": "eye-level medium close-up with soft background anamorphic bokeh, 85mm lens",
                "emotion": "composed, playful, amused intelligence, confident eye contact with the camera",
                "vo": '(Shin Yuri): "(playful, composed chuckle) One hundred million won? That\'s far too little to even put a down payment on an apartment in Seoul..."',
                "sfx": "soft city breeze, delicate fabric rustle",
            },
            {
                "time": "4.5s-6s",
                "label": "THE ESCALATION",
                "content": "split perspectives on the sidewalk: left angle shows reporter leaning in closer with microphone; right angle captures a perplexed young male citizen scratching his neck in bewildered thought",
                "camera": "fast lateral whip pan settling into a two-shot profile, 50mm lens",
                "emotion": "reporter eager for answers; interviewee blinking with furrowed brow",
                "vo": '(Street Reporter): "(probing, rapid-fire) A luxury sports car? A startup? Or would you play it safe and stash it away in savings?"',
                "sfx": "distant bicycle bell, pedestrian chatter",
            },
            {
                "time": "6s-8s",
                "label": "THE HOOK",
                "content": "tight macro close-up of the reporter\'s sharp gaze and confident grin; he leans directly toward the viewer as if addressing the camera itself",
                "camera": "intense direct frontal push-in, shallow depth-of-field, 85mm lens",
                "emotion": "magnetic, conspiratorial, lowering pitch for dramatic impact",
                "vo": '(Street Reporter): "(low, conspiratorial, leaning in) Final question... What if you were given the chance to become the richest person in the entire world?"',
                "sfx": "subtle bass riser swell, street noise fading into background",
            },
            {
                "time": "8s-10s",
                "label": "THE CLEVER REBUTTAL — END ON FREEZE FRAME",
                "content": "Shin Yuri crosses her arms, tilts her head with a stunning radiant smile, speaking directly into the microphone; background pedestrians blur into golden daylight bokeh; she finishes her sentence and holds her posture completely still",
                "camera": "slow dramatic push-in to tight portrait, settling into a locked static hold",
                "emotion": "sharp witty smirk, amused eyes sparkling with ambition",
                "vo": '(Shin Yuri): "(sharp, witty smirk) Before I answer that... why don\'t you tell me how to get that rich first?" · END ON A COMPLETE FREEZE FRAME: Shin Yuri holds her confident smile and locked gaze through 10s, zero extra movement.',
                "sfx": "deep dramatic cinematic hit, resonant bass fade to dead silence",
            },
        ],
    },
    {
        "block_num": 2,
        "title": "The Man Who Became Richest",
        "cast_mentions": ["@Kang Jin-Hoo", "@Female Interviewer", "@Spirit Shaman"],
        "description": f"VIDEO: E01 B2 — The Man Who Became Richest",
        "voice_ref": "English sophisticated male billionaire and female host",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE INTERVIEW",
                "content": "sleek ultra-modern television broadcast studio with floor-to-ceiling glass windows overlooking Seoul financial high-rises; FEMALE INTERVIEWER (poised, tailored navy blazer, dark bob) sits opposite KANG JIN-HOO (23yo Korean male, tailored midnight-navy bespoke three-piece suit, crisp white shirt, silk tie, tousled jet-black hair); multiple studio broadcast cameras frame them",
                "camera": "wide studio tracking dolly glide across glass studio table, 35mm lens",
                "emotion": "professional formality, tense broadcast atmosphere",
                "vo": '(Female Interviewer): "(poised, measured respect) You are the youngest person, and the very first Korean, to ever become the richest man in the world."',
                "sfx": "subtle studio room tone, quiet studio air hum",
            },
            {
                "time": "1.5s-3s",
                "label": "THE RUMOR",
                "content": "tight medium close-up of the female interviewer leaning forward over cue cards, looking intently into Jin-Hoo\'s calm eyes",
                "camera": "gentle slow push-in, 85mm portrait lens with soft studio backlighting",
                "emotion": "probing curiosity, testing boundaries with a daring question",
                "vo": '(Female Interviewer): "(low, intriguing tone) There are persistent rumors surrounding you... that you possess clairvoyance. That you can see the future."',
                "sfx": "soft rustle of cue card paper",
            },
            {
                "time": "3s-4.5s",
                "label": "THE DENIAL",
                "content": "close-up of Kang Jin-Hoo; he raises his left hand with a calm, gentle dismissive wave, smiling softly with absolute composure",
                "camera": "subtle Dutch angle push-in on Jin-Hoo\'s composed expression, 50mm lens",
                "emotion": "calm, self-deprecating modesty masking supreme inner confidence",
                "vo": '(Kang Jin-Hoo): "(calm, smooth, gentle chuckle) Seeing the future? There\'s no such thing. I\'m just an ordinary investor who trusts his timing."',
                "sfx": "faint low sub-drone pulsing beneath the audio",
            },
            {
                "time": "4.5s-6s",
                "label": "THE GOLDEN EYE",
                "content": "extreme macro close-up of Kang Jin-Hoo\'s right eye; his pupil dilates as a supernatural radiant amber-gold iris pattern ignites with mystical circuit rings; the studio lights around him suddenly shift into dark emerald shadows",
                "camera": "crash zoom into iris reflection, cinematic lens flare, 100mm macro lens",
                "emotion": "sudden supernatural shock, ancient perception awakening",
                "vo": '(Kang Jin-Hoo): "(internal voice, breathless whisper) ...My eye. The golden glow is awakening again."',
                "sfx": "ethereal high-frequency shimmer, deep mystical resonance pulse",
            },
            {
                "time": "6s-8s",
                "label": "THE APPARITION",
                "content": "surreal supernatural vision overlaying the television studio: behind the frozen studio crew, the ghostly SPIRIT SHAMAN in ancient ceremonial green and gold silk robes materializes in emerald mist, while a colossal radiant bald eagle with incandescent flaming wings ascends with a silent screech",
                "camera": "high-angle dynamic tilt down looking over the spirit eagle\'s blazing wing span",
                "emotion": "overwhelming sacred awe, ominous supernatural grandeur",
                "vo": '(Spirit Shaman): "(ancient, dual-layered spectral voice) You perceive the threads of destiny... but do you possess the courage to reshape them?"',
                "sfx": "rushing supernatural wind, burning flame crackle, ethereal eagle cry",
            },
            {
                "time": "8s-10s",
                "label": "THE COMPOSURE — END ON FREEZE FRAME",
                "content": "cut back to reality: Kang Jin-Hoo sits upright under the bright studio keylights, the golden glow in his eye fading back to piercing dark obsidian; he offers an enigmatic smirk to the interviewer, completely unfazed; studio crew continues filming",
                "camera": "locked eye-level medium close-up, dramatic split lighting",
                "emotion": "secretive, supreme confidence, veiled power",
                "vo": '(Kang Jin-Hoo): "(enigmatic, quiet confidence) ...I\'m just an ordinary man who knows when to place the winning bet." · END ON A COMPLETE FREEZE FRAME: Kang Jin-Hoo holds his locked smirk and unwavering gaze into the lens through 10s.',
                "sfx": "heavy orchestral thud, heart-beat thump, silence",
            },
        ],
    },
    {
        "block_num": 3,
        "title": "Before the Fortune",
        "cast_mentions": ["@Kang Jin-Hoo", "@Oh Taek-Gyu"],
        "description": f"VIDEO: E01 B3 — Before the Fortune",
        "voice_ref": "Young English male veteran and animated best friend",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE WAKING",
                "content": "flashback: cramped semi-basement apartment bedroom with worn floral wallpaper and morning sunlight filtering through high frosted barred street windows; 23yo KANG JIN-HOO wearing a plain cream crewneck sweater sits up on a worn floor mattress, rubbing his temple groggily",
                "camera": "low-angle establishing push-in across scattered moving boxes and worn linoleum, 28mm lens",
                "emotion": "drowsy exhaustion, lingering headache from military discharge",
                "vo": '(Kang Jin-Hoo): "(groggy, heavy sigh) Weeks have passed since my discharge from the army... yet the headache still pounds like an anvil."',
                "sfx": "distant street traffic outside window, rustle of coarse cotton bedsheets",
            },
            {
                "time": "1.5s-3s",
                "label": "THE DISCHARGE CAP",
                "content": "close-up of Jin-Hoo picking up his black military discharge service cap with embroidered insignia from a dusty shelf; he stares at it quietly, remembering the training accident that gave him the vision",
                "camera": "slow macro push-in on military insignia and calloused fingers, 50mm lens",
                "emotion": "somber contemplation, quiet resolve",
                "vo": '(Kang Jin-Hoo): "(somber whisper, quiet resolve) That bizarre accident during military training... that was where this nightmare began."',
                "sfx": "soft thud of cap setting down, quiet clock tick",
            },
            {
                "time": "3s-4.5s",
                "label": "THE INTRUSION",
                "content": "the apartment door swings open abruptly; OH TAEK-GYU (23yo Korean male, stocky build, gray zip-up hoodie over white tee, black square-rimmed glasses) barges in carrying a convenience store plastic bag and a worn notebook, huffing with frantic excitement",
                "camera": "medium shot framed from hallway doorway, rapid handheld pan, 35mm lens",
                "emotion": "manic geeky excitement, breathless urgency",
                "vo": '(Oh Taek-Gyu): "(breathless, shouting excitedly) Jin-Hoo! Are you awake?! You are not going to believe what I just dug up!"',
                "sfx": "door creak and slam, crinkling plastic convenience store bag",
            },
            {
                "time": "4.5s-6s",
                "label": "THE SPREAD",
                "content": "Taek-Gyu drops onto the low wooden coffee table, kicking aside old newspapers, spreading out an old USB drive, crumpled scraps of paper with alphanumeric codes, and a phone with an abstract trading chart",
                "camera": "top-down overhead bird\'s eye view table shot, 35mm lens",
                "emotion": "obsessive, frantic energy, tapping paper eagerly",
                "vo": '(Oh Taek-Gyu): "(rapid-fire manic chatter) Remember that Bantcoin we bought back in college before you enlisted? The one everyone mocked us for touching?!"',
                "sfx": "clatter of plastic USB drive on wood, paper rustling aggressively",
            },
            {
                "time": "6s-8s",
                "label": "THE KEY",
                "content": "medium close-up of Taek-Gyu leaning across the table, thrusting the small black USB drive in front of Jin-Hoo\'s face, his glasses catching window light",
                "camera": "tight dynamic over-the-shoulder push-in toward USB drive, 50mm lens",
                "emotion": "triumphant revelation, wide grins behind thick lenses",
                "vo": '(Oh Taek-Gyu): "(triumphant, conspiratorial whisper) I recovered the private encryption key to our forgotten wallet. Jin-Hoo... our account is still alive!"',
                "sfx": "metallic clink, low bass rumble beginning",
            },
            {
                "time": "8s-10s",
                "label": "THE REALIZATION — END ON FREEZE FRAME",
                "content": "Jin-Hoo stares at the USB drive in Taek-Gyu\'s palm; his eyes widen with sudden realization as the gravity of the forgotten asset sinks in; Taek-Gyu grins excitedly beside him; daylight streams across their frozen forms",
                "camera": "locked frontal two-shot, high contrast daylight chiaroscuro",
                "emotion": "stunned awakening, heart racing disbelief",
                "vo": '(Kang Jin-Hoo): "(stunned, heart dropping) ...Bantcoin? Exactly how many coins did we purchase back then?" · END ON A COMPLETE FREEZE FRAME: Jin-Hoo stares motionless at the key while Taek-Gyu freezes mid-laugh through 10s.',
                "sfx": "sharp dramatic musical sting, sudden silence with ringing reverb",
            },
        ],
    },
    {
        "block_num": 4,
        "title": "Thirteen Point Five Billion Won",
        "cast_mentions": ["@Kang Jin-Hoo", "@Oh Taek-Gyu"],
        "description": f"VIDEO: E01 B4 — Thirteen Point Five Billion Won",
        "voice_ref": "Two young English male voices realizing sudden fortune",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE LOGIN",
                "content": "medium shot over Jin-Hoo\'s shoulder: Taek-Gyu holds his smartphone horizontally over the wooden table, fingers typing an abstract pin on a dark cryptocurrency exchange interface with cyan glowing numbers",
                "camera": "macro over-the-shoulder Dutch angle tilt, 50mm lens",
                "emotion": "nervous tension, held breath, anticipation",
                "vo": '(Oh Taek-Gyu): "(nervous, gulping) Hold on... the exchange wallet is decrypting. Let\'s see what crumbs are left."',
                "sfx": "digital interface confirmation tone, finger tap on glass screen",
            },
            {
                "time": "1.5s-3s",
                "label": "THE NUMBERS",
                "content": "close-up of Taek-Gyu\'s face as the screen light flashes blue against his glasses lenses; his mouth drops open slack, his round eyes expanding into total shock; color drains from his cheeks",
                "camera": "slow crash push-in on Taek-Gyu\'s wide stunned eyes behind glasses, 85mm lens",
                "emotion": "pure unadulterated shock, speechlessness, paralysis",
                "vo": '(Oh Taek-Gyu): "(trembling whisper, voice cracking) Jin-Hoo... are my eyes completely playing tricks on me? Or is this screen malfunctioning?!"',
                "sfx": "high-pitched ringing tinnitus tone, muted room sound",
            },
            {
                "time": "3s-4.5s",
                "label": "THE CALCULATION",
                "content": "Jin-Hoo leans over the table, grabbing Taek-Gyu\'s wrist to steady the shaking phone; Jin-Hoo\'s brows furrow tightly as he rapidly calculates the conversion rates in his head",
                "camera": "medium tight two-shot, dynamic camera pan from hands to Jin-Hoo\'s intense face, 35mm lens",
                "emotion": "sharp calculating intellect, analytical disbelief giving way to awe",
                "vo": '(Kang Jin-Hoo): "(intense, calculating under breath) Three thousand coins... multiplied by the current real-time market spot price..."',
                "sfx": "rapid heartbeat pulse, low frequency sub-bass crescendo",
            },
            {
                "time": "4.5s-6s",
                "label": "THE BOMBSHELL",
                "content": "Taek-Gyu leaps to his feet, knocking his plastic chair backward onto the floor, clutching his head with both hands in hysterical disbelief",
                "camera": "low-angle wide shot capturing Taek-Gyu standing with arms raised, 24mm wide lens",
                "emotion": "hysterical hysteria, manic joy, screaming in a quiet neighborhood",
                "vo": '(Oh Taek-Gyu): "(screaming in manic disbelief) THIRTEEN POINT FIVE BILLION! 13.5 Billion Won! We are multi-billionaire moguls, Jin-Hoo!"',
                "sfx": "loud chair crashing on wooden floor, Taek-Gyu yelling echoes",
            },
            {
                "time": "6s-8s",
                "label": "THE PLEA",
                "content": "Taek-Gyu drops back to his knees beside Jin-Hoo, aggressively shaking Jin-Hoo\'s shoulders with an absurd, tearful comedic smile, begging him to confirm it\'s real",
                "camera": "medium close-up, comedic handheld shake, 50mm lens",
                "emotion": "desperate joy, uncontrollable trembling laughter",
                "vo": '(Oh Taek-Gyu): "(laughing and crying simultaneously) Tell me I\'m not dreaming! Slap me across the face, Jin-Hoo! Is this actually real?!"',
                "sfx": "fabric grabbing, heavy frantic breathing",
            },
            {
                "time": "8s-10s",
                "label": "THE GAZE UPWARD — END ON FREEZE FRAME",
                "content": "Jin-Hoo pulls away gently, looking down at the glowing phone screen and then up toward the ceiling as if peering through the roof into the city; his eyes turn cold, solemn, and intensely focused",
                "camera": "slow dramatic low-angle push-in on Jin-Hoo\'s unblinking profile",
                "emotion": "heavy solemn weight, sudden transformation from boy to mastermind",
                "vo": '(Kang Jin-Hoo): "(deep, cold, resolute) ...This is no dream. But if we aren\'t careful, a fortune like this can vanish in a single breath." · END ON A COMPLETE FREEZE FRAME: Jin-Hoo holds his cold penetrating stare while Taek-Gyu freezes holding the phone.',
                "sfx": "heavy orchestral impact, deep resonant brass hold, dead silence",
            },
        ],
    },
    {
        "block_num": 5,
        "title": "The Warning From Tomorrow",
        "cast_mentions": ["@Kang Jin-Hoo", "@Oh Taek-Gyu", "@Spirit Shaman"],
        "description": f"VIDEO: E01 B5 — The Warning From Tomorrow",
        "voice_ref": "Young English visionary and spiritual omen",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE VISION BURST",
                "content": "sudden supernatural reality warp: the cramped apartment dissolves into a tempest of blazing golden-pink fire and ash; a massive incandescent SPIRIT EAGLE with colossal wingspan shrieks silently above Jin-Hoo\'s head, casting blazing golden rim-light over his body",
                "camera": "dynamic upward rotating tilt around Jin-Hoo, 24mm wide angle",
                "emotion": "overwhelming supernatural intensity, visual sensory overload",
                "vo": '(Kang Jin-Hoo): "(internal gasp, trembling) ...It\'s back! The flaming eagle of tomorrow!"',
                "sfx": "blazing fire roar, rushing wind vortex, ethereal eagle cry",
            },
            {
                "time": "1.5s-3s",
                "label": "THE BURNING LETTERS",
                "content": "across the smoky sky within Jin-Hoo\'s trance, burning crimson embers form blazing typography: \'MOUNTAINHILL EXCHANGE\' followed by a massive shattered padlock and the burning omen \'CRITICAL FAILURE / BANKRUPTCY\'",
                "camera": "tracking shot sweeping across blazing molten typography in midair, 50mm lens",
                "emotion": "urgent dread, catastrophic premonition, impending doom",
                "vo": '(Spirit Shaman): "(haunting, reverberating spectral warning) The corporate tower you place your trust in... will crumble into ash before sundown."',
                "sfx": "searing metal hiss, explosive ember pop, ominous low bass drone",
            },
            {
                "time": "3s-4.5s",
                "label": "THE INQUIRY",
                "content": "the vision snaps violently back to the reality of the small apartment; Jin-Hoo stumbles forward, panting heavily with sweat beading on his forehead; he grabs Taek-Gyu\'s hoodie collar with fierce intensity",
                "camera": "sudden crash cut to medium tight profile, handheld shake, 35mm lens",
                "emotion": "feverish urgency, desperate life-or-death intensity",
                "vo": '(Kang Jin-Hoo): "(panting, desperate grip) Taek-Gyu! Which exchange holds our cryptocurrency assets right now?! Tell me!"',
                "sfx": "heavy panting, violent collar grab rustle, sharp intake of air",
            },
            {
                "time": "4.5s-6s",
                "label": "THE ANSWER",
                "content": "Taek-Gyu blinks in terror at Jin-Hoo\'s suddenly terrifying expression, stammering with wide eyes as he holds his phone defensively",
                "camera": "close-up of Taek-Gyu\'s sweating face, 50mm lens",
                "emotion": "confused terror, startled by his best friend\'s ferocity",
                "vo": '(Oh Taek-Gyu): "(stammering, confused, scared) M-Mountainhill Exchange... the biggest, most trusted platform in Korea. Why, Jin-Hoo?!"',
                "sfx": "faint clock ticking underneath like a countdown bomb",
            },
            {
                "time": "6s-8s",
                "label": "THE COMMAND",
                "content": "Jin-Hoo slams his palm flat onto the wooden coffee table, pointing directly at the exchange app on Taek-Gyu\'s screen with burning resolve; his right eye reflects a faint phantom golden ember",
                "camera": "low-angle dramatic tilt up on Jin-Hoo towering over the table, 35mm lens",
                "emotion": "absolute commanding authority, no room for hesitation",
                "vo": '(Kang Jin-Hoo): "(authoritative, commanding roar) Liquidate everything immediately! Sell every single Bantcoin before noon!"',
                "sfx": "heavy fist slam on wood, reverberating bass drop",
            },
            {
                "time": "8s-10s",
                "label": "THE IMPOSSIBLE DEMAND — END ON FREEZE FRAME",
                "content": "Taek-Gyu stares in agonizing hesitation with his thumb hovering over the sell button, torn between thirteen billion won and his best friend\'s terrifying warning; Jin-Hoo stands completely motionless over him, burning with absolute certainty",
                "camera": "intense split-focus two-shot, thumb trembling over the screen, Jin-Hoo\'s cold face in background",
                "emotion": "paralyzing conflict, high-stakes countdown",
                "vo": '(Kang Jin-Hoo): "(cold, deadly serious whisper) Put your trust in me... wait another hour and we lose everything we just found." · END ON A COMPLETE FREEZE FRAME: Taek-Gyu freezes with trembling thumb over the button while Jin-Hoo glares down through 10s.',
                "sfx": "ticking clock abrupt stop, heavy dark cello sustain into silence",
            },
        ],
    },
    {
        "block_num": 6,
        "title": "The Future Is Real",
        "cast_mentions": ["@Kang Jin-Hoo", "@Oh Taek-Gyu"],
        "description": f"VIDEO: E01 B6 — The Future Is Real",
        "voice_ref": "English news anchor and shocked friends",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE SELL ORDER",
                "content": "close-up of Taek-Gyu\'s sweating thumb slamming down onto a glowing blue confirmation button on the phone screen; a clean green banner flashes: \'SELL ORDER EXECUTED — 100% CASH TRANSFERRED TO BANK ACCOUNT\'",
                "camera": "macro close-up on glass screen tap with rapid pull-back, 100mm lens",
                "emotion": "reckless desperate leap of faith, trembling relief",
                "vo": '(Oh Taek-Gyu): "(gasping, nervous exhales) It\'s done! The sell order cleared and the cash hit our bank... but Jin-Hoo, are you positive about this?"',
                "sfx": "digital transaction confirmation chime, heavy exhale",
            },
            {
                "time": "1.5s-3s",
                "label": "THE SERVER CRASH",
                "content": "just thirty seconds later: the phone screen suddenly flickers violently with red error bars, flashing an abrupt error pop-up: \'502 BAD GATEWAY — MOUNTAINHILL SERVERS UNREACHABLE — WITHDRAWALS SUSPENDED\'",
                "camera": "extreme macro zoom on phone screen displaying red flashing error banner, 85mm lens",
                "emotion": "sudden chilling shock, reality crashing down",
                "vo": '(Oh Taek-Gyu): "(voice trembling, eyes widening in panic) W-Wait... the app just crashed. 502 Bad Gateway?! Mountainhill\'s entire server network just went dead?!"',
                "sfx": "harsh digital error glitch buzz, rising siren tone",
            },
            {
                "time": "3s-4.5s",
                "label": "THE NEWS BREAK",
                "content": "Taek-Gyu frantically switches to a live news stream on his laptop: a red breaking news ticker scrolls across the screen showing police cars outside Mountainhill headquarters: \'BREAKING: CEO FLEES COUNTRY — EXCHANGE SUSPENDS WITHDRAWALS\'",
                "camera": "fast whip pan from phone to flickering laptop screen, 35mm lens",
                "emotion": "absolute dread, jaw dropped in horror, hands trembling violently",
                "vo": '(News Anchor on Laptop): "(urgent breaking news report) Breaking news: South Korea\'s largest crypto exchange has abruptly collapsed amid allegations of massive insolvency and executive flight!"',
                "sfx": "urgent television breaking news siren fanfare, news anchor audio filter",
            },
            {
                "time": "4.5s-6s",
                "label": "THE REALIZATION",
                "content": "Taek-Gyu slowly turns around from the laptop to look at Jin-Hoo standing in the center of the dark apartment; Taek-Gyu\'s face is pale white, shaking uncontrollably in disbelief that they escaped with their cash just minutes before the crash",
                "camera": "slow dramatic low-angle dolly push-in toward Jin-Hoo through Taek-Gyu\'s shoulder, 50mm lens",
                "emotion": "awe, terror, reverent shock, realizing his best friend predicted the future",
                "vo": '(Oh Taek-Gyu): "(shaking uncontrollably, breathless awe) You foresaw it... you knew this collapse would happen before anyone else. Who on earth are you, Jin-Hoo?!"',
                "sfx": "deep haunting sub-bass swell, muffled ambient room tone",
            },
            {
                "time": "6s-8s",
                "label": "THE CONFESSION",
                "content": "close-up of Kang Jin-Hoo; he turns his head slowly toward Taek-Gyu, his expression completely composed, serene, and terrifyingly calm under the morning light cutting through the basement window",
                "camera": "tight cinematic portrait push-in, 85mm prime lens with rich natural shadows",
                "emotion": "calm, burdened, prophetic certainty, shedding all deception",
                "vo": '(Kang Jin-Hoo): "(calm, deep, prophetic whisper) I told you earlier, Taek-Gyu... this was never just a lucky guess."',
                "sfx": "subtle mystical golden chime, heartbeat pulse",
            },
            {
                "time": "8s-10s",
                "label": "THE CLIFFHANGER — END ON FREEZE FRAME",
                "content": "Jin-Hoo steps forward, his right eye flashing with an unmistakable golden supernatural spark; he raises his head with supreme ambition, looking directly into the camera lens with a piercing, predatory smile; background apartment fades into dramatic contrast",
                "camera": "slow hero push-in directly into Jin-Hoo\'s golden gleaming eye, settling into locked hold",
                "emotion": "unyielding ambition, the birth of the world\'s greatest future investor",
                "vo": '(Kang Jin-Hoo): "(cold, chilling, triumphant delivery) I see the future. And this is merely the opening move." · END ON A COMPLETE FREEZE FRAME: Jin-Hoo locks his golden eye onto the lens, motionless through 10s, cliffhanger freeze.',
                "sfx": "massive cinematic bass drop, dramatic orchestral hit, sudden hard cut to silence",
            },
        ],
    },
]


def format_full_block_prompt(block: dict) -> str:
    """Build the exact 10s multi-line prompt conforming to PROMPT_CONTRACT v3 in 100% English."""
    mentions_line = " ".join(block["cast_mentions"])
    header = f'SERYE DRAMA BLOCK — {SERIES_TITLE} — Block {block["block_num"]} "{block["title"]}" (10s, {len(block["beats"])} beats)'
    inputs = f"INPUTS: attached image ingredients = faces of {', '.join(block['cast_mentions'])} only (ref-locked). This text walkthrough is the sole structural guide. Animate strictly following the time-labeled beats below. Each character wears EXACTLY the wardrobe stated in their beat and matches their attached reference face exactly."

    lines = [mentions_line, header, inputs, ""]
    for b in block["beats"]:
        beat_str = (
            f'{b["time"]} — {b["label"]}: {b["content"]} · CAMERA: {b["camera"]} · '
            f'EMOTION: {b["emotion"]} · VO: {b["vo"]} · SFX: {b["sfx"]}'
        )
        lines.append(beat_str)
        lines.append("")

    return "\n".join(lines).strip()


def build_char_refs_csv(output_path: Path):
    """Build char_refs_investor.csv (cols: prompt,scene name) for Flow image queue in English."""
    chars = [
        (
            "CHARACTER: KANG JIN-HOO (investor_who_sees_the_future)",
            "KANG JIN-HOO, 23-year-old Korean male, lead protagonist. Recently discharged military veteran, lean athletic build, fair complexion, short textured tousled jet-black hair with natural fringe, sharp intelligent hooded dark eyes, defined jawline, restrained understated calm expression. WARDROBE: cream long-sleeve crewneck pullover sweater, dark indigo slim jeans, clean white low-top sneakers. Full body three-quarter standing studio portrait, clean neutral gray background, cinematic 85mm portrait lighting, ultra-realistic digital webtoon manhwa aesthetics, masterwork fine art fidelity, photorealistic skin pores.",
        ),
        (
            "CHARACTER: OH TAEK-GYU (investor_who_sees_the_future)",
            "OH TAEK-GYU, 23-year-old Korean male, co-investor and best friend. Stocky slightly chubby build, round friendly face, short neat dark hair, thick black rectangular eyeglasses, expressive animated eyebrows, warm energetic comedic personality. WARDROBE: heather-gray zip-up hoodie over plain white crewneck t-shirt, dark charcoal casual trousers, comfortable sneakers. Full body three-quarter standing studio portrait, neutral studio background, 85mm soft studio key lighting, premium digital manhwa aesthetics.",
        ),
        (
            "CHARACTER: STREET REPORTER (investor_who_sees_the_future)",
            "STREET REPORTER, young Korean male in early 20s, television news vox-pop host. Slim athletic build, neat jet-black side-parted styled hair, sharp handsome face, charismatic broadcast smile, expressive dark eyes. WARDROBE: tailored charcoal-gray two-piece suit jacket, matching trousers, crisp white collared dress shirt, slim black tie, holding matte-black handheld microphone with blue foam windscreen. Three-quarter studio portrait, professional television studio lighting.",
        ),
        (
            "CHARACTER: SHIN YURI (investor_who_sees_the_future)",
            "SHIN YURI, young Korean female in early 20s, elegant confident pedestrian interviewee. Long voluminous wavy honey-blonde hair with soft curtain bangs, warm almond-shaped hazel-brown eyes, fair radiant complexion, enchanting intelligent smile, delicate gold hoop earrings. WARDROBE: tailored beige collared silk button-up blouse, understated professional chic styling. Three-quarter bust studio portrait, warm golden hour softbox lighting.",
        ),
        (
            "CHARACTER: FEMALE INTERVIEWER (investor_who_sees_the_future)",
            "FEMALE INTERVIEWER, young Korean female in late 20s, premier broadcast television host. Poised elegant posture, neat chin-length styled dark obsidian bob haircut, refined symmetrical facial features, piercing calm inquisitive dark eyes, subtle makeup. WARDROBE: tailored navy blue structured blazer, dark silk inner blouse, holding leather-bound interview cue cards. Formal broadcast studio three-quarter portrait.",
        ),
        (
            "CHARACTER: SPIRIT SHAMAN (investor_who_sees_the_future)",
            "SPIRIT SHAMAN, ancient supernatural Korean spiritual entity. Aged dignified weathered facial features, piercing luminescent pale jade-green eyes, ceremonial headdress with jade beads, ornate layered dark green and gold embroidered silk hanbok robes, surrounded by subtle ethereal green mist and embers. Beside the shaman, a magnificent supernatural bald eagle with blazing incandescent golden-pink flame wings and sharp amber eyes. Mystical fantasy portrait.",
        ),
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["prompt", "scene name"])
        for scene_name, prompt in chars:
            writer.writerow([prompt, scene_name])


def main():
    out_dir = Path("/home/john/manga-reviews/output/the-investor-who-sees-the-future/ch1/flow_queue")
    out_dir.mkdir(parents=True, exist_ok=True)

    episode_csv_path = out_dir / "e01.csv"
    char_refs_path = out_dir / "char_refs_investor.csv"

    # 1. Build character references CSV
    build_char_refs_csv(char_refs_path)
    print(f"[OK] Character references CSV: {char_refs_path}")

    # 2. Build individual block prompts and queue CSVs
    episode_rows = []
    for b in BLOCKS_DATA:
        b_num = b["block_num"]
        prompt_text = format_full_block_prompt(b)

        # Save individual .txt prompt file
        txt_path = out_dir / f"block{b_num}_video_prompt.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(prompt_text + "\n")

        row = {
            "prompt": prompt_text,
            "description": b["description"],
            "hashtags": HASHTAGS,
            "videoModel": MODEL,
            "videoMode": MODE,
            "videoDurationSeconds": DURATION,
            "flowQuantity": QUANTITY,
            "videoVoiceReference": b["voice_ref"],
            "flowAspectRatio": ASPECT,
        }
        episode_rows.append(row)

        # Save individual per-block queue CSV
        block_csv_path = out_dir / f"block{b_num}_queue.csv"
        with open(block_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
            writer.writeheader()
            writer.writerow(row)

        print(f"  - Block {b_num}: {txt_path.name} & {block_csv_path.name}")

    # 3. Build Episode CSV (e01.csv)
    with open(episode_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        for r in episode_rows:
            writer.writerow(r)

    print(f"\n[OK] Episode 1 Full Flow Automator CSV (6 Blocks) [100% ENGLISH]: {episode_csv_path}")

    # 4. Mirror to serye directory
    serye_episodes_csv = Path("/home/john/serye/investor_episodes_csv")
    serye_episodes_csv.mkdir(parents=True, exist_ok=True)
    with open(serye_episodes_csv / "e01.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        for r in episode_rows:
            writer.writerow(r)
    print(f"[OK] Mirrored to /home/john/serye/investor_episodes_csv/e01.csv")


if __name__ == "__main__":
    main()
