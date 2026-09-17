#!/usr/bin/env python3
"""
build_chapter2_production.py — Master Production Suite for Chapter 2.
Applies all optimizations and safety fixes established in Chapter 1:
- 100% natural, crisp English voice acting and dialogue.
- Enforced authentic 2D Korean webtoon manhwa anime animation style.
- Full-bleed 9:16 vertical video (no comic panels, no borders, no split screen).
- 10-second drama blocks with exact timestamped beats (0s-1.5s, 1.5s-3s, 3s-4.5s, 4.5s-6s, 6s-8s, 8s-10s).
- Explicit freeze-frame ending directive on every block.
- Character @mentions (@Kang Jin-Hoo, @Oh Taek-Gyu, @Drill Sergeant, @Spirit Shaman).
- 100% policy-hardened against reputational risk / current events filter.
- Outputs both .txt (with @@@NEXT@@@) and .csv (Flow Automator Max V3 schema).
- Generates clean 9:16 panel crops for reference.
"""

import os
import sys
import csv
import json
from pathlib import Path
from PIL import Image

BASE_DIR = Path("/home/john/manga-reviews/output/the-investor-who-sees-the-future/ch2")
FLOW_DIR = BASE_DIR / "flow_queue"
CROPS_DIR = BASE_DIR / "clean_frame_crops"
IMAGES_DIR = BASE_DIR / "images"

FLOW_DIR.mkdir(parents=True, exist_ok=True)
CROPS_DIR.mkdir(parents=True, exist_ok=True)

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

HASHTAGS = "#manhwa #2danime #webtoon #investorWhoSeesTheFuture #koreanAnime #shortDrama"
MODEL = "Omni Flash"
MODE = "ingredients"
DURATION = "10"
QUANTITY = "1"
ASPECT = "9:16"
DELIMITER = "\n\n@@@NEXT@@@\n\n"

STYLE_HEADER = (
    "Art style: authentic 2D Korean webtoon manhwa anime animation. Crisp clean dark ink line art, "
    "vibrant flat cel-shaded coloring, authentic manhwa character features, fluid 2D anime animation aesthetic. "
    "STRICTLY NOT 3D render, NOT live-action CGI, NOT photorealistic, NOT western comic book style. "
    "Full-bleed 9:16 vertical video. Smooth continuous animation across the 10-second sequence. "
    "Strictly NO comic panels, NO border frames, NO split screen, NO multi-panel collage, "
    "NO on-screen subtitles, NO speech bubbles, NO watermark."
)

BLOCKS_DATA = [
    {
        "block_num": 1,
        "title": "The Mortar Range Drill",
        "cast_mentions": ["@Kang Jin-Hoo", "@Drill Sergeant"],
        "description": "VIDEO: E02 B1 — The Mortar Range Drill",
        "voice_ref": "Barks of military sergeant and young disciplined soldier",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE PROLOGUE",
                "action": "Flashback to one year ago: high-angle panoramic establishing shot over a sun-baked South Korean army artillery firing range nestled between rugged forested mountains. A battery of 81mm mortar tubes stands anchored into packed earth trenches with green ammunition crates.",
                "camera": "Slow crane down through heat distortion haze into mortar firing line, 28mm lens",
                "lighting": "Harsh midday summer sunlight 5600K, dusty atmospheric haze, deep terrain shadows",
                "vo": '(Narrator): "(solemn, reflective documentary cadence) One year ago... Mortar Firing Range, Infantry Regiment. Where the impossible began."',
                "sfx": "Distant thundering artillery concussions echoing across hills, dry mountain wind",
            },
            {
                "time": "1.5s-3s",
                "label": "THE REPRIMAND",
                "action": "Medium shot: a hardened DRILL SERGEANT in full digital camouflage fatigues, tactical helmet, and dark sunglasses storms forward, aggressively pointing his leather-gloved finger at Private Kang Jin-Hoo standing rigid at attention beside the mortar tube.",
                "camera": "Dynamic low-angle lateral tracking shot framing the commanding officer, 35mm lens",
                "lighting": "Sharp directional sun casting hard shadows beneath helmet brim",
                "vo": '(Drill Sergeant): "(furious, gravelly military bark) Private Kang Jin-Hoo! Wipe that distracted daze off your face and focus on your weapon!"',
                "sfx": "Heavy combat boots crunching on gravel, leather gear rustle",
            },
            {
                "time": "3s-4.5s",
                "label": "THE SALUTE",
                "action": "Close-up of young Private Kang Jin-Hoo (sweat beading down cheekbones under green Kevlar helmet, camouflage face paint, intense disciplined dark eyes) snapping a razor-sharp salute with unwavering posture.",
                "camera": "Locked eye-level portrait shot, 50mm prime lens",
                "emotion": "Disciplined military obedience masking sudden strange distraction",
                "vo": '(Kang Jin-Hoo): "(disciplined, loud military shout) Private Kang Jin-Hoo! Yes, Drill Sergeant, Sir!"',
                "sfx": "Snappy fabric slap of military salute, deep intake of breath",
            },
            {
                "time": "4.5s-6s",
                "label": "THE GLIMMER",
                "action": "As Jin-Hoo returns to handling the mortar ammunition, his gaze involuntarily shifts toward the dense pine treeline behind the firing pits; a faint supernatural golden light glints between the dark evergreen branches.",
                "camera": "Slow Dutch angle push-in past Jin-Hoo\'s helmet brim toward the distant tree canopy, 50mm lens",
                "emotion": "Perplexed curiosity, gut instinct tingling",
                "vo": '(Kang Jin-Hoo): "(internal whisper, confused breath) Huh...? Up there in the trees... what is that light?"',
                "sfx": "Faint ethereal metallic chime hidden beneath the wind, soft breeze through needles",
            },
            {
                "time": "6s-8s",
                "label": "THE TREE LINE",
                "action": "Subjective POV through Jin-Hoo\'s eyes: deep within the shadowy pine boughs, an otherworldly golden creature perches silently, its eyes glowing like molten embers through the swaying needles.",
                "camera": "Telephoto crash zoom into the dark tree canopy, 85mm lens",
                "lighting": "Deep shadowy forest green pierced by a single beam of radiant golden aura",
                "vo": '(Kang Jin-Hoo): "(whispering in disbelief under breath) Is that... an eagle? Why is it glowing like fire?"',
                "sfx": "Subtle low sub-bass pulse, distant raven call muffled",
            },
            {
                "time": "8s-10s",
                "label": "THE SIGHTING — END ON FREEZE FRAME",
                "action": "Jin-Hoo stands completely frozen beside his mortar crew, one hand on the ammunition crate, staring wide-eyed into the mountain ridge as the golden radiance intensifies; his squadmate continues prepping ammunition unaware.",
                "camera": "Slow dramatic push-in to Jin-Hoo\'s stunned face, settling into a locked hold",
                "emotion": "Stunned paralysis, the calm before the storm",
                "vo": '(Kang Jin-Hoo): "(intense, trembling murmur) Did eagles always look like that...?" · END ON COMPLETE FREEZE FRAME: Jin-Hoo holds his frozen stare into the forest, motionless through 10s.',
                "sfx": "High-pitched ringing frequency, abrupt dead silence",
            },
        ],
    },
    {
        "block_num": 2,
        "title": "The Golden Warning",
        "cast_mentions": ["@Kang Jin-Hoo"],
        "description": "VIDEO: E02 B2 — The Golden Warning",
        "voice_ref": "Young soldier witnessing supernatural omen",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE SWOOP",
                "action": "Sudden explosive motion: the colossal radiant GOLDEN EAGLE launches from the pine canopy, streaking downward in a blinding trail of golden lightning across the firing range sky, visible only to Jin-Hoo.",
                "camera": "High-speed sweeping pan following the fiery golden streak across the sky, 24mm wide lens",
                "lighting": "Blinding golden-pink flash illuminating the entire mountain basin",
                "vo": '(Kang Jin-Hoo): "(alarmed gasp, stumbling back) W-What is that?! Look out!"',
                "sfx": "Crackling lightning boom, rushing sonic air displacement",
            },
            {
                "time": "1.5s-3s",
                "label": "THE INQUIRY",
                "action": "Jin-Hoo ducks and frantically reaches out to grab his squadmate\'s tactical vest, pointing wildly into the empty blue sky above their heads with trembling hands.",
                "camera": "Medium two-shot tracking Jin-Hoo\'s agitated gesture, 35mm lens",
                "emotion": "Frantic urgency met with complete peer confusion",
                "vo": '(Kang Jin-Hoo): "(frantic, pointing upward) Hey! Did you just see that massive golden eagle fly right over us?!"',
                "sfx": "Tactical nylon rustle, heavy soldier breathing",
            },
            {
                "time": "3s-4.5s",
                "label": "THE SQUAD REACTION",
                "action": "Close-up of his squadmate looking up at the empty blue sky, blinking blankly, then looking back at Jin-Hoo with an amused, baffled shake of his helmeted head.",
                "camera": "Over-the-shoulder reaction shot, 50mm portrait lens",
                "lighting": "Bright midday sun washing over blank camouflage helmets",
                "vo": '(Squadmate): "(confused chuckle, bewildered) Where? There\'s nothing up there except sun, Jin-Hoo. You getting heatstroke?"',
                "sfx": "Chuckle breath, distant mortar crew shouting range commands",
            },
            {
                "time": "4.5s-6s",
                "label": "THE AR HUD HUD APPEARANCE",
                "action": "Extreme macro close-up of Jin-Hoo\'s eyes: glowing holographic amber-gold geometric characters and floating warning reticles materialize right in his visual field, displaying the designation \'81MM MORTAR TUBE KM187\' surrounded by flashing red exclamation marks.",
                "camera": "Extreme macro zoom on Jin-Hoo\'s contracting pupil, 100mm macro lens",
                "lighting": "Amber-gold holographic HUD reflection dancing inside his dark iris",
                "vo": '(Kang Jin-Hoo): "(breathless, terrified whisper) What is this...? Augmented reality in the middle of live-fire drill...? No... this is inside my eyes!"',
                "sfx": "High-tech digital hum, soft pulsing sonar ping",
            },
            {
                "time": "6s-8s",
                "label": "THE COUNTDOWN",
                "action": "Through Jin-Hoo\'s glowing vision, a burning golden outline surrounds the steel mortar barrel at his feet; flashing red numerals count down from \'03... 02...\' accompanied by an ominous thermal warning glow.",
                "camera": "Low-angle tilted shot looking at the steel mortar tube shrouded in ghostly crimson energy, 35mm lens",
                "lighting": "Supernatural red warning aura bleeding into realistic military trench",
                "vo": '(Kang Jin-Hoo): "(heart pounding violently) The tube... the mortar barrel is going to rupture!"',
                "sfx": "Rapid heartbeat accelerating to 180 BPM, rising warning frequency",
            },
            {
                "time": "8s-10s",
                "label": "THE LIVE SHELL PREP — END ON FREEZE FRAME",
                "action": "A squad loader lifts a heavy olive-drab 81mm mortar shell, aligning its fins over the muzzle; Jin-Hoo\'s body locks in sheer primal horror, watching the shell begin its fatal drop.",
                "camera": "Slow dramatic macro push-in on the steel shell descending over the muzzle, locking into a frozen hold",
                "lighting": "Harsh metallic glint on the shell casing, high-contrast trench shadows",
                "vo": '(Kang Jin-Hoo): "(internal scream of mortal terror) STOP! DON\'T DROP IT!" · END ON COMPLETE FREEZE FRAME: The shell freezes millimeters above the muzzle while Jin-Hoo lunges forward.',
                "sfx": "Deep resonant brass swell, sudden terrifying vacuum silence",
            },
        ],
    },
    {
        "block_num": 3,
        "title": "The Mortar Catastrophe",
        "cast_mentions": ["@Kang Jin-Hoo"],
        "description": "VIDEO: E02 B3 — The Mortar Catastrophe",
        "voice_ref": "Heroic soldier saving squad from fatal explosion",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE INSTINCT",
                "action": "The live shell slides into the steel mortar tube. Jin-Hoo\'s survival instinct takes over before thought—every muscle in his body explodes into motion as he propels himself toward his comrades.",
                "camera": "Dynamic ground-level tracking shot moving with Jin-Hoo\'s desperate lunge, 24mm wide angle",
                "lighting": "High-speed shutter capturing airborne dirt and gravel kicked up by his boots",
                "vo": '(Narrator): "(intense, breathless gravitas) When a human being senses their life is in mortal peril... the body moves before the mind can think."',
                "sfx": "Violent gravel kick, sharp intake of breath",
            },
            {
                "time": "1.5s-3s",
                "label": "THE DESPERATE DIVE",
                "action": "Jin-Hoo slams his body sideways into his two squadmates, tackling them off the concrete firing pad and down into the protective earth trench, covering them with his own body.",
                "camera": "Low-angle heroic tracking pan following the three bodies crashing into the dirt, 35mm lens",
                "emotion": "Selfless heroic panic, pure adrenaline",
                "vo": '(Kang Jin-Hoo): "(raw, throat-shredding scream) GET DOWN!! EVERYBODY HIT THE GROUND!!" ',
                "sfx": "Heavy impact of three bodies crashing onto packed dirt, gear rattling violently",
            },
            {
                "time": "3s-4.5s",
                "label": "THE DETONATION",
                "action": "Catastrophic failure: the mortar tube ruptures at the base with a deafening apocalyptic fireball; jagged steel shrapnel and black smoke tear outward in an omnidirectional shockwave across the pad.",
                "camera": "Violent camera shake with slow-motion shockwave ripple tearing across screen, 28mm lens",
                "lighting": "Blinding orange-white explosion flash obliterating all ambient shadows",
                "vo": '(Narrator): "(grim, thunderous impact) A catastrophic barrel breach. In a split second, life and death were decided."',
                "sfx": "Deafening explosive detonation concussion, tearing metal screech",
            },
            {
                "time": "4.5s-6s",
                "label": "THE SHIELD",
                "action": "Inside the trench, Jin-Hoo curls tightly over his squadmates as black smoke, burning debris, and red-hot shrapnel blast overhead; a glowing golden shield pattern flickers faintly across his back for a microsecond.",
                "camera": "Tight claustrophobic angle inside the dust-filled trench, 50mm lens",
                "lighting": "Fiery orange rim light cutting through billowing black smoke and falling dirt",
                "vo": '(Squadmates under him): "(screaming in terror and shock) AAAHHH! WHAT HAPPENED?!"',
                "sfx": "Whistling shrapnel ricocheting off rocks, shower of heavy dirt clods falling",
            },
            {
                "time": "6s-8s",
                "label": "THE WOUND",
                "action": "Jin-Hoo winces in sharp agony as a flying fragment grazes the right side of his face; blood trickles down his temple, but his right eye under the blood blazes with pure radiant gold.",
                "camera": "Close-up of Jin-Hoo\'s face through swirling smoke, 85mm prime lens",
                "emotion": "Agony mixed with miraculous survival, golden eye glowing through soot",
                "vo": '(Kang Jin-Hoo): "(pained, gritted teeth groan) Ugh...! My face... my eye!"',
                "sfx": "Ringing high-pitch ear trauma whine (tinnitus), muffled groans of survivors",
            },
            {
                "time": "8s-10s",
                "label": "THE HERO SILHOUETTE — END ON FREEZE FRAME",
                "action": "Jin-Hoo slowly lifts his head from the smoking crater edge; his comrades beneath him are alive and uninjured; through the drifting ash, Jin-Hoo\'s single golden eye pierces the black smoke toward the sky, holding a heroic freeze.",
                "camera": "Slow heroic low-angle push-in on Jin-Hoo\'s blood-streaked, soot-covered face",
                "lighting": "God rays of sunlight piercing the black smoke column, golden eye gleaming brightly",
                "vo": '(Narrator): "(solemn, epic realization) He saved his squad... but paid the price with his sight. Or so the doctors believed." · END ON COMPLETE FREEZE FRAME: Jin-Hoo holds his gaze through the smoke motionless.',
                "sfx": "Massive deep orchestral choir chord, slow fade into silent ringing tone",
            },
        ],
    },
    {
        "block_num": 4,
        "title": "The Awakening of the Eye",
        "cast_mentions": ["@Kang Jin-Hoo"],
        "description": "VIDEO: E02 B4 — The Awakening of the Eye",
        "voice_ref": "Young veteran realizing his supernatural clairvoyance",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE HOSPITAL RECOVERY",
                "action": "Military hospital ward: Jin-Hoo lies in a bed with clean white bandages wrapped around his right eye and forehead; a sterile sunlight washes over the clean blue hospital blanket.",
                "camera": "High-angle slow push-in toward hospital bed, 35mm lens",
                "lighting": "Clean sterile daylight, cool blue and white hospital tones",
                "vo": '(Narrator): "(calm, reflective) Discharged with an honorable medical retirement. One eye scarred... yet seeing more than any human alive."',
                "sfx": "Gentle hospital monitor beeping, quiet curtain rustle",
            },
            {
                "time": "1.5s-3s",
                "label": "THE BANDAGE REMOVAL",
                "action": "Jin-Hoo slowly unwraps the white gauze bandage from his right eye in front of a mirror; the scar is visible, but the iris beneath has transformed into an intricate, radiant golden ring.",
                "camera": "Over-the-shoulder mirror reflection shot, 50mm portrait lens",
                "lighting": "Directional bathroom light highlighting the radiant golden iris",
                "vo": '(Kang Jin-Hoo): "(hushed, reverent awe) The doctors called it nerve damage... but this isn\'t blindness. This is something else."',
                "sfx": "Soft unwinding of cotton gauze, subtle mystical chime",
            },
            {
                "time": "3s-4.5s",
                "label": "THE STREET TEST",
                "action": "Walking through a crowded city crosswalk in casual clothes, Jin-Hoo looks around: floating golden data arcs and probability percentages shimmer faintly over street signs and pedestrian pathways.",
                "camera": "Fluid handheld tracking shot gliding beside Jin-Hoo in crowd, 35mm lens",
                "lighting": "Warm afternoon city sunlight, golden holographic data glyphs floating in air",
                "vo": '(Kang Jin-Hoo): "(fascinated, rapidly analyzing) Every choice, every outcome... I can see the probabilities before they happen."',
                "sfx": "Subtle digital data stream whoosh, city pedestrian chatter",
            },
            {
                "time": "4.5s-6s",
                "label": "THE CRYPTO MEMORY",
                "action": "Jin-Hoo stops dead in his tracks on the sidewalk as a sudden vivid memory flash hits him: Taek-Gyu laughing in college, holding up their Bantcoin receipt.",
                "camera": "Rapid Dutch angle crash zoom into Jin-Hoo\'s widening eyes, 85mm lens",
                "lighting": "Flash of memory golden lighting contrasting current street shadows",
                "vo": '(Kang Jin-Hoo): "(realization hitting like lightning) That crypto wallet Taek-Gyu bought... it wasn\'t just luck. It was the first link in the chain!"',
                "sfx": "Thunderous bass heartbeat hit, digital connection chime",
            },
            {
                "time": "6s-8s",
                "label": "THE STRIDE FORWARD",
                "action": "Jin-Hoo turns on his heel with intense newfound purpose, striding purposefully down the sidewalk toward his apartment, his coat fluttering in the breeze.",
                "camera": "Low-angle dynamic tracking shot leading in front of Jin-Hoo, 35mm lens",
                "lighting": "Golden hour sunlight crowning his head, determined facial contours",
                "vo": '(Kang Jin-Hoo): "(cold, focused resolve) I\'m not going to live as a crippled veteran. I\'m going to use this eye to take everything."',
                "sfx": "Fast confident footsteps on concrete, sweeping orchestral swell",
            },
            {
                "time": "8s-10s",
                "label": "THE MASTERMIND SMILE — END ON FREEZE FRAME",
                "action": "Jin-Hoo pauses at the entrance to his basement building, looking up at the Seoul skyline towers, flashing a confident predatory smile as his golden eye gleams, locking into a heroic freeze.",
                "camera": "Slow dramatic low-angle push-in, locking into a frozen hero pose",
                "lighting": "Deep dramatic chiaroscuro shadow, golden eye shining like a beacon",
                "vo": '(Kang Jin-Hoo): "(quiet, triumphant ambition) Watch me rewrite the financial world." · END ON COMPLETE FREEZE FRAME: Jin-Hoo holds his sharp smile motionless through 10s.',
                "sfx": "Epic cinematic brass hit, reverberating silence",
            },
        ],
    },
    {
        "block_num": 5,
        "title": "The Thirteen Billion Reality",
        "cast_mentions": ["@Kang Jin-Hoo", "@Oh Taek-Gyu"],
        "description": "VIDEO: E02 B5 — The Thirteen Billion Reality",
        "voice_ref": "Two young men in apartment celebrating confirmed fortune",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE BANK CONFIRMATION",
                "action": "Return to present day: inside the semi-basement apartment, Taek-Gyu stares at his laptop screen showing an official bank balance with a row of ten digits: 13,500,000,000 KRW safely deposited in government-insured savings accounts.",
                "camera": "Macro over-the-shoulder Dutch angle tracking down to glowing bank balance, 50mm lens",
                "lighting": "Clean screen glow illuminating their astonished faces in dim room",
                "vo": '(Oh Taek-Gyu): "(gasping in pure euphoria) It\'s really in the bank! Not crypto tokens anymore... cold, clean, untouchable cash!"',
                "sfx": "Digital bank confirmation notification chime, celebratory desk slap",
            },
            {
                "time": "1.5s-3s",
                "label": "THE SPREADSHEET",
                "action": "Taek-Gyu furiously opens a digital spreadsheet, adjusting asset allocations and profit splits while laughing hysterically with uncontainable manic glee.",
                "camera": "Close-up of Taek-Gyu\'s manic grin and rapidly clicking fingers on keyboard, 50mm lens",
                "lighting": "Bright screen light bouncing off his thick glasses",
                "vo": '(Oh Taek-Gyu): "(hysterical laughter, giddy) Fifty-fifty split! That\'s over six billion won each! Jin-Hoo, we never have to work another day in our lives!"',
                "sfx": "Rapid mechanical keyboard clatter, celebratory squeal",
            },
            {
                "time": "3s-4.5s",
                "label": "THE PROTAGONIST COUNTER",
                "action": "Medium shot: Kang Jin-Hoo sits calmly across the table, sipping black coffee from a ceramic mug, completely unimpressed by early retirement.",
                "camera": "Eye-level medium shot, smooth slow push-in, 50mm lens",
                "lighting": "Natural morning sunlight cutting through basement window bars",
                "vo": '(Kang Jin-Hoo): "(calm, smooth, visionary) Retire? Six billion won is just seed money, Taek-Gyu. This is where the real game begins."',
                "sfx": "Ceramic coffee mug clicking onto table, quiet breeze",
            },
            {
                "time": "4.5s-6s",
                "label": "THE QUESTION TO JIN-HOO",
                "action": "Taek-Gyu stops typing, spins his chair around, and stares at Jin-Hoo with wide, bewildered eyes, unable to comprehend his friend\'s appetite.",
                "camera": "Tight reaction close-up of Taek-Gyu scratching his ear in shock, 85mm lens",
                "emotion": "Disbelief turning into eager excitement",
                "vo": '(Oh Taek-Gyu): "(baffled, leaning forward) Seed money?! Thirteen billion is seed money to you?! What on earth are you planning to buy next?!"',
                "sfx": "Chair swivel squeak, paper rustling",
            },
            {
                "time": "6s-8s",
                "label": "THE NOTEBOOK OPEN",
                "action": "Jin-Hoo pulls out a clean black leather-bound notebook, sliding it across the wooden table; on the page, names of premier tech conglomerates and pharmaceutical firms are neatly penned.",
                "camera": "Top-down bird\'s eye view of the notebook sliding smoothly across the wood, 35mm lens",
                "lighting": "Crisp morning light illuminating handwritten financial targets",
                "vo": '(Kang Jin-Hoo): "(deep, authoritative strategy) We aren\'t playing with volatile coins anymore. We\'re going after undervalued public corporations."',
                "sfx": "Smooth leather notebook slide on wood, pen click",
            },
            {
                "time": "8s-10s",
                "label": "THE PARTNERSHIP — END ON FREEZE FRAME",
                "action": "Taek-Gyu leans over the notebook, his face illuminated with newfound respect and ambition; Jin-Hoo extends his right hand across the table for a handshake, locking into a frozen covenant.",
                "camera": "Dramatic profile two-shot: extended hand between two ambitious young men",
                "lighting": "Golden morning sunbeam bridging the space between their hands",
                "vo": '(Oh Taek-Gyu): "(awe, determined grin) If you can see tomorrow... then count me in until the very end." · END ON COMPLETE FREEZE FRAME: Their hands lock in a firm grip, motionless through 10s.',
                "sfx": "Firm handclap impact, deep resonant orchestral chord hold, silence",
            },
        ],
    },
    {
        "block_num": 6,
        "title": "The Next Target",
        "cast_mentions": ["@Kang Jin-Hoo", "@Oh Taek-Gyu", "@Spirit Shaman"],
        "description": "VIDEO: E02 B6 — The Next Target",
        "voice_ref": "The visionary investor revealing his next multi-billion strike",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE WALL MAP",
                "action": "Jin-Hoo stands before a large wall map of Seoul\'s central business district, dotted with corporate headquarters, financial towers, and market indicators.",
                "camera": "Slow low-angle push-in on Jin-Hoo\'s commanding back silhouette, 35mm lens",
                "lighting": "Moody cinematic atmosphere, soft daylight filtering across the corporate map",
                "vo": '(Kang Jin-Hoo): "(internal voice, sharp analysis) In two weeks, a biotech firm will announce an FDA breakthrough that nobody sees coming."',
                "sfx": "Quiet room tone, rustle of map paper",
            },
            {
                "time": "1.5s-3s",
                "label": "THE RESEARCH PROMPT",
                "action": "Taek-Gyu looks up the company on his financial terminal: the stock chart shows a depressed, forgotten valuation trading at historical lows.",
                "camera": "Macro shot of terminal screen with cyan candlesticks, fast whip pan to Taek-Gyu, 50mm lens",
                "lighting": "Cool cyan screen glow washing over Taek-Gyu\'s glasses",
                "vo": '(Oh Taek-Gyu): "(skeptical, furrowed brow) Dong-jin Pharmaceuticals? Jin-Hoo, their stock has been flatlining for three consecutive quarters!"',
                "sfx": "Rapid mouse scroll clicks, analytical hum",
            },
            {
                "time": "3s-4.5s",
                "label": "THE SPIRITUAL VISION",
                "action": "Behind Jin-Hoo, the supernatural golden Spirit Shaman flickers into existence for a heartbeat, pointing an ancient claw toward the pharmaceutical company\'s logo on the wall.",
                "camera": "Ethereal low-angle camera shift with green mist swirling, 35mm lens",
                "lighting": "Emerald and golden mystical light dancing across the wall map",
                "vo": '(Spirit Shaman): "(reverberating spectral whisper) The seed has been planted... the harvest will be staggering."',
                "sfx": "Sacred chime pulse, mystical wind gust",
            },
            {
                "time": "4.5s-6s",
                "label": "THE INSTRUCTION",
                "action": "Jin-Hoo turns to Taek-Gyu with utter certainty, planting his finger firmly on the stock ticker on the screen.",
                "camera": "Dynamic two-shot, camera pushing into Jin-Hoo\'s unwavering eye, 50mm lens",
                "lighting": "Dramatic split light, shadows highlighting Jin-Hoo\'s confident jaw",
                "vo": '(Kang Jin-Hoo): "(commanding, calm conviction) Dump every single won into their shares tomorrow at market open. All thirteen billion."',
                "sfx": "Heavy table tap, low sub-bass riser swell",
            },
            {
                "time": "6s-8s",
                "label": "THE SHOCKED ACCEPTANCE",
                "action": "Taek-Gyu gasps, then grins with reckless thrill, nodding his head aggressively as he keys in the pre-market order parameters.",
                "camera": "Close-up of Taek-Gyu\'s excited eyes behind glasses, 85mm lens",
                "emotion": "Adrenaline-fueled trust, jumping off the cliff together",
                "vo": '(Oh Taek-Gyu): "(thrilled, crazy laughter) All in! We\'re betting the entire fortune! You crazy bastard, let\'s do it!"',
                "sfx": "Rapid keystrokes, digital pre-order confirmation beep",
            },
            {
                "time": "8s-10s",
                "label": "THE GOLDEN EYE PROPHET — END ON FREEZE FRAME",
                "action": "Jin-Hoo steps directly in front of the lens; his right eye flares with brilliant incandescent gold, piercing the camera with supreme, undeniable dominance as the skyline towers reflect in his pupil.",
                "camera": "Slow dramatic hero push-in directly into the blazing golden eye, locking into a frozen frame at 10s",
                "lighting": "Pure golden mystical aura igniting his silhouette, background fading into black",
                "vo": '(Kang Jin-Hoo): "(cold, chilling, victorious prophecy) The world thinks I got lucky. Next week, they\'ll realize I own the board." · END ON COMPLETE FREEZE FRAME: Jin-Hoo holds his golden piercing gaze motionless.',
                "sfx": "Massive cinematic orchestral drop, epic brass chord hold, sudden dead silence",
            },
        ],
    },
]


def format_block_prompt(block: dict) -> str:
    """Build the exact 10s multi-beat walkthrough containing all timestamps in 100% English."""
    mentions = " ".join(block["cast_mentions"])
    header = f'SERYE DRAMA BLOCK — The Investor Who Sees The Future — Chapter 2 — Block {block["block_num"]} "{block["title"]}" (10s, 6 beats)'
    inputs = (
        f"INPUTS: attached image ingredients = faces of {', '.join(block['cast_mentions'])} only (ref-locked). "
        "Animate strictly following the time-labeled beats below:"
    )

    lines = [mentions, STYLE_HEADER, "", header, inputs, ""]
    for b in block["beats"]:
        lighting = b.get("lighting") or b.get("emotion") or "Natural cinematic 2D cel-shaded lighting"
        line = (
            f'{b["time"]} — {b["label"]}: {b["action"]} · '
            f'CAMERA: {b["camera"]} · LIGHTING: {lighting} · '
            f'VO: {b["vo"]} · SFX: {b["sfx"]}'
        )
        lines.append(line)
        lines.append("")

    return "\n".join(lines).strip()


def crop_clean_panels():
    """Extract clean 9:16 crops from Chapter 2 webtoon pages for reference."""
    print("[CROPS] Generating clean, borderless 9:16 reference images from Chapter 2...")
    for b in BLOCKS_DATA:
        b_num = b["block_num"]
        # Map block to approximate page (14 pages total across 6 blocks)
        page_num = min(14, max(1, (b_num - 1) * 2 + 1))
        page_path = IMAGES_DIR / f"page_{page_num:03d}.webp"
        out_crop = CROPS_DIR / f"ch02_b{b_num:02d}_{b['title'].lower().replace(' ', '_')[:25]}.png"

        if out_crop.exists():
            continue

        if not page_path.exists():
            continue

        try:
            im = Image.open(page_path)
            w, h = im.size
            crop_h = int(w * (16 / 9))
            box = (0, 0, w, min(h, crop_h))
            cropped = im.crop(box)
            cropped.save(out_crop, "PNG")
            print(f"  [OK] Cropped: {out_crop.name}")
        except Exception as e:
            print(f"  [WARN] Failed to crop {page_path.name}: {e}")


def main():
    crop_clean_panels()

    block_prompts = []
    episode_rows = []

    for b in BLOCKS_DATA:
        prompt_text = format_block_prompt(b)
        block_prompts.append(prompt_text)

        # Per-block individual txt file
        p_txt = FLOW_DIR / f"block{b['block_num']}_prompts.txt"
        with open(p_txt, "w", encoding="utf-8") as f:
            f.write(prompt_text + "\n")

        episode_rows.append({
            "prompt": prompt_text,
            "description": b["description"],
            "hashtags": HASHTAGS,
            "videoModel": MODEL,
            "videoMode": MODE,
            "videoDurationSeconds": DURATION,
            "flowQuantity": QUANTITY,
            "videoVoiceReference": b["voice_ref"],
            "flowAspectRatio": ASPECT,
        })

    # 1. Master continuous 10s blocks .txt (separated by @@@NEXT@@@)
    cont_txt_path = FLOW_DIR / "flow_6_continuous_blocks.txt"
    with open(cont_txt_path, "w", encoding="utf-8") as f:
        f.write(DELIMITER.join(block_prompts) + "\n")
    print(f"[OK] Chapter 2 Master 10s Blocks TXT: {cont_txt_path}")

    # 2. Save e02.csv
    e02_csv_path = FLOW_DIR / "e02.csv"
    with open(e02_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        for r in episode_rows:
            writer.writerow(r)
    print(f"[OK] Chapter 2 e02.csv (V3 Schema): {e02_csv_path}")

    # 3. Mirror to serye directory
    serye_dir = Path("/home/john/serye/investor_episodes_csv")
    serye_dir.mkdir(parents=True, exist_ok=True)
    with open(serye_dir / "e02.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        for r in episode_rows:
            writer.writerow(r)
    print(f"[OK] Mirrored to /home/john/serye/investor_episodes_csv/e02.csv")


if __name__ == "__main__":
    main()
