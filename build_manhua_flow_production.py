#!/usr/bin/env python3
"""
build_manhua_flow_production.py — Production Suite for Google Flow Video Generation.

Fixes two critical production issues:
1. ART STYLE: Strictly enforces 2D Korean webtoon / manhwa anime illustration style
   (crisp dark ink linework, vibrant flat cel-shading, 2D animation fluidity,
   strictly NOT 3D, NOT photorealistic, NOT live-action CGI).
2. SINGLE-FRAME COMPOSITION: Ensures the video generator generates videos frame-by-frame
   (or as continuous single-shot scenes). The multi-panel storyboard is strictly a
   director's blueprint guide and is NEVER rendered inside the video.
   Zero comic borders, zero split screens, zero on-screen text or timestamps.

Outputs:
1. flow_frame_by_frame_queue.csv — 36 individual shots (each beat is its own video generation row)
2. block1_frames.csv .. block6_frames.csv — Per-block 6-shot queues
3. flow_continuous_10s_queue.csv — 6 blocks formatted as continuous single-camera 10s shots
4. clean_frame_crops/ — Clean single-panel 9:16 reference images extracted from original chapter
"""

import os
import sys
import csv
import json
from pathlib import Path
from PIL import Image

BASE_DIR = Path("/home/john/manga-reviews/output/the-investor-who-sees-the-future/ch1")
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
ASPECT = "9:16"

# Core style directive to be injected into every prompt
MANHUA_STYLE_DIRECTIVE = (
    "Art style: authentic 2D Korean webtoon manhwa anime animation. Crisp clean dark ink line art, "
    "vibrant flat cel-shaded coloring, authentic manhwa character features, fluid 2D anime animation aesthetic. "
    "STRICTLY NOT 3D render, NOT live-action CGI, NOT photorealistic, NOT western comic book style. "
    "Full-bleed 9:16 vertical single continuous shot. Strictly NO comic panels, NO border frames, "
    "NO split screen, NO multi-panel collage, NO on-screen subtitles, NO speech bubbles, NO watermark."
)

# 36 individual frames structured across the 6 blocks
FRAMES_DATA = [
    # --- BLOCK 1: The Question That Changes Everything ---
    {
        "block": 1,
        "beat": 1,
        "time": "0s-1.5s",
        "title": "Street Interview Opening",
        "cast": "@Street Reporter",
        "desc": "Wide crane shot descending into a bustling modern Seoul pedestrian shopping street plaza. Street Reporter stands in center wearing charcoal suit, holding blue microphone. Pedestrians stroll in background.",
        "camera": "Slow cinematic crane down from high angle into eye-level medium-wide tracking, 24mm equivalent lens",
        "lighting": "Bright diffused daylight 5600K, clean urban glass reflections, soft shadows",
        "vo": '(Street Reporter): "(energetic, crisp broadcast projection) Have you ever wondered what you would do if a fortune landed in your hands overnight?"',
        "sfx": "Bustling city street ambiance, distant chatter, footsteps on stone pavement",
        "page": 1,
        "duration": "5",
    },
    {
        "block": 1,
        "beat": 2,
        "time": "1.5s-3s",
        "title": "The Hundred Million Won Question",
        "cast": "@Street Reporter",
        "desc": "Medium close-up of the Street Reporter stepping forward enthusiastically, extending blue microphone toward the viewer with an engaging, theatrical challenge smile.",
        "camera": "Dynamic low-angle smooth push-in toward reporter and microphone, 35mm lens",
        "lighting": "Bright daytime sunlight with clean anime cel-shading, crisp highlights on suit",
        "vo": '(Street Reporter): "(dramatic, teasing, eyes wide) What if you suddenly received one hundred million won in cold hard cash?!"',
        "sfx": "Microphone movement whoosh, faint surprised crowd murmur",
        "page": 1,
        "duration": "5",
    },
    {
        "block": 1,
        "beat": 3,
        "time": "3s-4.5s",
        "title": "Shin Yuri Thoughtful Reaction",
        "cast": "@Shin Yuri",
        "desc": "Medium shot of Shin Yuri with long wavy honey-blonde hair and beige silk blouse pausing on the sidewalk. She rests one finger on her chin, gazing warmly into the camera with effortless intelligence.",
        "camera": "Eye-level medium close-up with soft background urban bokeh, 85mm portrait lens",
        "lighting": "Warm afternoon sunlight, delicate rim light on honey-blonde hair strands",
        "vo": '(Shin Yuri): "(playful, composed chuckle) One hundred million won? That\'s far too little to even put a down payment on an apartment in Seoul..."',
        "sfx": "Gentle city breeze, soft fabric rustle",
        "page": 2,
        "duration": "5",
    },
    {
        "block": 1,
        "beat": 4,
        "time": "4.5s-6s",
        "title": "Pedestrian Street Options",
        "cast": "@Street Reporter",
        "desc": "Street Reporter turns to interview a young male pedestrian who scratches his head in comical bewilderment while contemplating the sudden wealth.",
        "camera": "Dynamic medium two-shot tracking camera moving subtly between reporter and pedestrian, 50mm lens",
        "lighting": "Natural midday sunlight, clean storefront reflections in background",
        "vo": '(Street Reporter): "(probing, rapid-fire) A luxury sports car? A startup? Or would you play it safe and stash it away in savings?"',
        "sfx": "Bicycle bell ding in distance, pedestrian chatter",
        "page": 1,
        "duration": "5",
    },
    {
        "block": 1,
        "beat": 5,
        "time": "6s-8s",
        "title": "The World Richest Hook",
        "cast": "@Street Reporter",
        "desc": "Intense close-up of the Street Reporter leaning directly toward the camera, lowering his tone with a sharp, conspiratorial grin.",
        "camera": "Direct frontal slow push-in focusing tightly on eyes and microphone, 85mm prime lens",
        "lighting": "High-contrast street lighting, dramatic shadow under jawline",
        "vo": '(Street Reporter): "(low, conspiratorial, leaning in) Final question... What if you were given the chance to become the richest person in the entire world?"',
        "sfx": "Subtle deep bass swell, ambient street noise fading down",
        "page": 2,
        "duration": "5",
    },
    {
        "block": 1,
        "beat": 6,
        "time": "8s-10s",
        "title": "Shin Yuri Clever Smirk Freeze",
        "cast": "@Shin Yuri",
        "desc": "Close-up of Shin Yuri crossing her arms, smiling with a sharp, ambitious sparkle in her eyes as she delivers her witty comeback, settling into a completely still, confident hero pose.",
        "camera": "Slow dramatic push-in to tight portrait, locking into a frozen static frame",
        "lighting": "Golden hour glow accentuating her smile and honey-blonde hair, creamy background blur",
        "vo": '(Shin Yuri): "(sharp, witty smirk) Before I answer that... why don\'t you tell me how to get that rich first?" · END ON COMPLETE FREEZE FRAME: She holds her confident smile motionless.',
        "sfx": "Punchy dramatic musical sting, crisp sudden silence with reverberating echo",
        "page": 2,
        "duration": "5",
    },

    # --- BLOCK 2: The Man Who Became Richest ---
    {
        "block": 2,
        "beat": 1,
        "time": "0s-1.5s",
        "title": "The High-Rise TV Studio",
        "cast": "@Female Interviewer @Kang Jin-Hoo",
        "desc": "Wide shot inside a luxury television broadcast studio with panoramic glass windows overlooking Seoul high-rises at dusk. Female Interviewer in navy blazer faces Kang Jin-Hoo in bespoke midnight-navy suit.",
        "camera": "Smooth lateral dolly glide along the glass interview table, 35mm lens",
        "lighting": "Professional TV studio key lighting mixed with cool blue twilight city view",
        "vo": '(Female Interviewer): "(poised, measured respect) You are the youngest person, and the very first Korean, to ever become the richest man in the world."',
        "sfx": "Quiet broadcast studio room hum, soft studio air conditioning tone",
        "page": 3,
        "duration": "5",
    },
    {
        "block": 2,
        "beat": 2,
        "time": "1.5s-3s",
        "title": "The Clairvoyance Rumor",
        "cast": "@Female Interviewer",
        "desc": "Medium close-up of the Female Interviewer leaning slightly forward over leather cue cards, looking with inquisitive piercing eyes across the table.",
        "camera": "Slow deliberate push-in on interviewer\'s face, 85mm portrait lens",
        "lighting": "Soft studio beauty lighting, crisp catchlights in her dark eyes",
        "vo": '(Female Interviewer): "(low, intriguing tone) There are persistent rumors surrounding you... that you possess clairvoyance. That you can see the future."',
        "sfx": "Subtle rustle of cue card paper, tense silence",
        "page": 3,
        "duration": "5",
    },
    {
        "block": 2,
        "beat": 3,
        "time": "3s-4.5s",
        "title": "Jin-Hoo Calm Denial",
        "cast": "@Kang Jin-Hoo",
        "desc": "Close-up of Kang Jin-Hoo raising his hand in a relaxed, modest gesture, smiling with serene self-possession against the twilight city backdrop.",
        "camera": "Subtle low-angle push-in on Jin-Hoo\'s handsome, composed expression, 50mm lens",
        "lighting": "Cool evening city light rimming his tousled black hair, warm studio key on cheek",
        "vo": '(Kang Jin-Hoo): "(calm, smooth, gentle chuckle) Seeing the future? There\'s no such thing. I\'m just an ordinary investor who trusts his timing."',
        "sfx": "Faint low-frequency sub drone beginning to vibrate",
        "page": 3,
        "duration": "5",
    },
    {
        "block": 2,
        "beat": 4,
        "time": "4.5s-6s",
        "title": "The Golden Eye Ignition",
        "cast": "@Kang Jin-Hoo",
        "desc": "Extreme macro close-up of Kang Jin-Hoo\'s right eye. His pupil contracts as radiant amber-gold mystical energy ignites within his iris, swirling with supernatural circuit patterns.",
        "camera": "Intense macro zoom directly into glowing golden iris, 100mm lens",
        "lighting": "Studio light dims into dark emerald shadow, golden iris illuminates his brow",
        "vo": '(Kang Jin-Hoo): "(internal whisper, breathless) ...My eye. The golden glow is awakening again."',
        "sfx": "Ethereal high-frequency shimmer, deep resonant magical pulse",
        "page": 3,
        "duration": "5",
    },
    {
        "block": 2,
        "beat": 5,
        "time": "6s-8s",
        "title": "The Flaming Spirit Eagle Apparition",
        "cast": "@Spirit Shaman",
        "desc": "Surreal supernatural apparition: behind the frozen studio set, a ghostly Spirit Shaman in ornate green-gold robes emerges from emerald mist, while a colossal radiant bald eagle with incandescent flaming wings ascends with power.",
        "camera": "High-angle dynamic tilt down looking over the spirit eagle\'s blazing wingspan, 24mm wide angle",
        "lighting": "Blazing golden-pink flame aura contrasting mystical emerald green mist",
        "vo": '(Spirit Shaman): "(ancient, reverberating spectral voice) You perceive the threads of destiny... but do you possess the courage to reshape them?"',
        "sfx": "Rushing supernatural wind vortex, crackling sacred fire, distant eagle shriek",
        "page": 4,
        "duration": "5",
    },
    {
        "block": 2,
        "beat": 6,
        "time": "8s-10s",
        "title": "The Enigmatic Smirk Freeze",
        "cast": "@Kang Jin-Hoo",
        "desc": "Cut back to reality in the TV studio: Kang Jin-Hoo sits upright under normal studio lighting, his golden eye fading back to dark obsidian as he offers a chillingly confident smirk directly into the camera.",
        "camera": "Locked eye-level medium close-up, dramatic high-contrast studio lighting",
        "lighting": "Crisp studio keylight, soft city bokeh behind",
        "vo": '(Kang Jin-Hoo): "(enigmatic, quiet confidence) ...I\'m just an ordinary man who knows when to place the winning bet." · END ON COMPLETE FREEZE FRAME: Jin-Hoo holds his locked smirk and unwavering gaze.',
        "sfx": "Heavy orchestral impact, deep heartbeat thump, silence",
        "page": 5,
        "duration": "5",
    },

    # --- BLOCK 3: Before the Fortune ---
    {
        "block": 3,
        "beat": 1,
        "time": "0s-1.5s",
        "title": "The Waking Veteran",
        "cast": "@Kang Jin-Hoo",
        "desc": "Inside a modest semi-basement apartment, 23yo Kang Jin-Hoo in a cream long-sleeve crewneck sweater sits up on his floor mattress, rubbing his temple groggily as morning light filters through high frosted windows.",
        "camera": "Low-angle establishing push-in across scattered moving boxes and worn linoleum, 28mm lens",
        "lighting": "Soft pale morning sunlight, gentle dust motes floating in sunbeam",
        "vo": '(Kang Jin-Hoo): "(groggy, heavy sigh) Weeks have passed since my discharge from the army... yet the headache still pounds like an anvil."',
        "sfx": "Distant city street hum outside window, rustle of cotton bedsheets",
        "page": 6,
        "duration": "5",
    },
    {
        "block": 3,
        "beat": 2,
        "time": "1.5s-3s",
        "title": "The Military Discharge Cap",
        "cast": "@Kang Jin-Hoo",
        "desc": "Close-up of Jin-Hoo picking up his black military discharge service cap with embroidered golden insignia from a shelf, gazing at it quietly with deep memories.",
        "camera": "Slow macro push-in on military insignia and calloused fingers, 50mm lens",
        "lighting": "Directional morning light casting clean shadows across the cap fabric",
        "vo": '(Kang Jin-Hoo): "(somber whisper, quiet resolve) That bizarre accident during military training... that was where this nightmare began."',
        "sfx": "Soft thud of cap setting down on wood, quiet wall clock tick",
        "page": 7,
        "duration": "5",
    },
    {
        "block": 3,
        "beat": 3,
        "time": "3s-4.5s",
        "title": "Taek-Gyu Sudden Entry",
        "cast": "@Oh Taek-Gyu",
        "desc": "The apartment door swings open wide. Oh Taek-Gyu in a gray zip-up hoodie over white tee and black glasses barges inside, holding a plastic convenience store bag and huffing with manic excitement.",
        "camera": "Medium shot framed from hallway doorway, rapid handheld pan, 35mm lens",
        "lighting": "Hallway daylight silhouetting Taek-Gyu\'s stocky energetic frame",
        "vo": '(Oh Taek-Gyu): "(breathless, shouting excitedly) Jin-Hoo! Are you awake?! You are not going to believe what I just dug up!"',
        "sfx": "Door latch click and swing open, crinkling plastic convenience store bag",
        "page": 8,
        "duration": "5",
    },
    {
        "block": 3,
        "beat": 4,
        "time": "4.5s-6s",
        "title": "Spreading the Clues",
        "cast": "@Oh Taek-Gyu",
        "desc": "Taek-Gyu drops to his knees at the low coffee table, excitedly setting down a small black USB flash drive, crumpled notebook papers, and his smartphone showing a clean crypto chart.",
        "camera": "Overhead high-angle view looking down at table items, 35mm lens",
        "lighting": "Warm interior daylight, clean cell shading on table items",
        "vo": '(Oh Taek-Gyu): "(rapid-fire manic chatter) Remember that Bantcoin we bought back in college before you enlisted? The one everyone mocked us for touching?!"',
        "sfx": "Plastic USB drive clatter on wood, paper rustling aggressively",
        "page": 9,
        "duration": "5",
    },
    {
        "block": 3,
        "beat": 5,
        "time": "6s-8s",
        "title": "The USB Key Revealed",
        "cast": "@Oh Taek-Gyu",
        "desc": "Medium close-up of Taek-Gyu thrusting the black USB drive forward in his palm, grinning triumphantly as sunlight glints off his thick spectacle lenses.",
        "camera": "Tight dynamic over-the-shoulder push-in toward USB drive in palm, 50mm lens",
        "lighting": "Bright morning light reflecting on glasses, joyful anime cel-shading",
        "vo": '(Oh Taek-Gyu): "(triumphant, conspiratorial whisper) I recovered the private encryption key to our forgotten wallet. Jin-Hoo... our account is still alive!"',
        "sfx": "Metallic key clink, subtle low-frequency bass swell",
        "page": 10,
        "duration": "5",
    },
    {
        "block": 3,
        "beat": 6,
        "time": "8s-10s",
        "title": "Jin-Hoo Awakening Realization",
        "cast": "@Kang Jin-Hoo @Oh Taek-Gyu",
        "desc": "Frontal two-shot: Jin-Hoo stares down at the USB drive in shock, his eyes widening as the math connects in his mind, while Taek-Gyu grins excitedly beside him, freezing into a clean held pose.",
        "camera": "Locked frontal medium two-shot with high-contrast morning light",
        "lighting": "Clean morning sunbeams highlighting their faces and table",
        "vo": '(Kang Jin-Hoo): "(stunned, heart dropping) ...Bantcoin? Exactly how many coins did we purchase back then?" · END ON COMPLETE FREEZE FRAME: Jin-Hoo stares motionless at the key.',
        "sfx": "Dramatic musical hit, sudden ringing silence",
        "page": 10,
        "duration": "5",
    },

    # --- BLOCK 4: Thirteen Point Five Billion Won ---
    {
        "block": 4,
        "beat": 1,
        "time": "0s-1.5s",
        "title": "Decrypting the Wallet",
        "cast": "@Oh Taek-Gyu @Kang Jin-Hoo",
        "desc": "Medium shot over Jin-Hoo\'s shoulder: Taek-Gyu holds his phone horizontally, fingers typing an abstract pin into a dark exchange interface with glowing cyan numbers.",
        "camera": "Macro over-the-shoulder Dutch angle tilt, 50mm lens",
        "lighting": "Cyan screen glow casting soft blue light on their hands and faces",
        "vo": '(Oh Taek-Gyu): "(nervous, gulping) Hold on... the exchange wallet is decrypting. Let\'s see what crumbs are left."',
        "sfx": "Digital interface confirmation chime, rapid screen tap clicks",
        "page": 11,
        "duration": "5",
    },
    {
        "block": 4,
        "beat": 2,
        "time": "1.5s-3s",
        "title": "The Disbelief on Screen",
        "cast": "@Oh Taek-Gyu",
        "desc": "Close-up of Taek-Gyu\'s face illuminated by bright blue screen glow; his jaw hangs slack, round eyes wide in paralyzing shock as color drains from his cheeks.",
        "camera": "Slow crash push-in on Taek-Gyu\'s wide stunned eyes behind glasses, 85mm lens",
        "lighting": "Intense cool blue screen reflection on his glasses and forehead",
        "vo": '(Oh Taek-Gyu): "(trembling whisper, voice cracking) Jin-Hoo... are my eyes completely playing tricks on me? Or is this screen malfunctioning?!"',
        "sfx": "High-pitched ringing tinnitus tone, muted room ambiance",
        "page": 11,
        "duration": "5",
    },
    {
        "block": 4,
        "beat": 3,
        "time": "3s-4.5s",
        "title": "The Analytical Calculation",
        "cast": "@Kang Jin-Hoo",
        "desc": "Jin-Hoo leans forward over the table, gripping Taek-Gyu\'s wrist to steady the shaking phone, his dark eyes sharp and intensely calculating conversion rates.",
        "camera": "Medium tight two-shot, dynamic whip pan from shaking hands to Jin-Hoo\'s intense face, 35mm lens",
        "lighting": "Dramatic split light, one side bathed in blue screen glow, other in morning sun",
        "vo": '(Kang Jin-Hoo): "(intense, calculating under breath) Three thousand coins... multiplied by the current real-time market spot price..."',
        "sfx": "Rapid heartbeat pulse, rising sub-bass swell",
        "page": 12,
        "duration": "5",
    },
    {
        "block": 4,
        "beat": 4,
        "time": "4.5s-6s",
        "title": "Taek-Gyu Hysterical Scream",
        "cast": "@Oh Taek-Gyu",
        "desc": "Taek-Gyu leaps to his feet, kicking his chair back against the floor, clutching his head with both hands and screaming in ecstatic manic joy.",
        "camera": "Low-angle wide shot capturing Taek-Gyu standing with arms raised, 24mm wide lens",
        "lighting": "Bright apartment interior, dynamic anime speed lines radiating outward",
        "vo": '(Oh Taek-Gyu): "(screaming in manic disbelief) THIRTEEN POINT FIVE BILLION! 13.5 Billion Won! We are multi-billionaire moguls, Jin-Hoo!"',
        "sfx": "Plastic chair clattering to the floor, Taek-Gyu shouting echoes",
        "page": 13,
        "duration": "5",
    },
    {
        "block": 4,
        "beat": 5,
        "time": "6s-8s",
        "title": "Slap Me Across the Face",
        "cast": "@Oh Taek-Gyu @Kang Jin-Hoo",
        "desc": "Taek-Gyu drops back to his knees, shaking Jin-Hoo\'s shoulders vigorously with a ridiculous, tearful comedic smile, begging to know if it\'s real.",
        "camera": "Medium close-up, energetic comedic handheld shake, 50mm lens",
        "lighting": "Warm morning apartment light, comical tear streaks on Taek-Gyu\'s cheeks",
        "vo": '(Oh Taek-Gyu): "(laughing and crying simultaneously) Tell me I\'m not dreaming! Slap me across the face, Jin-Hoo! Is this actually real?!"',
        "sfx": "Fabric grabbing rustle, heavy frantic breathing and laughter",
        "page": 13,
        "duration": "5",
    },
    {
        "block": 4,
        "beat": 6,
        "time": "8s-10s",
        "title": "Jin-Hoo Resolute Stare Freeze",
        "cast": "@Kang Jin-Hoo",
        "desc": "Jin-Hoo gently pulls away, staring down at the glowing phone and then upward toward the ceiling, his eyes turning cold, calculating, and intensely focused into a locked freeze.",
        "camera": "Slow dramatic low-angle push-in on Jin-Hoo\'s unblinking profile",
        "lighting": "Moody chiaroscuro shadow cutting across Jin-Hoo\'s jawline",
        "vo": '(Kang Jin-Hoo): "(deep, cold, resolute) ...This is no dream. But if we aren\'t careful, a fortune like this can vanish in a single breath." · END ON COMPLETE FREEZE FRAME.',
        "sfx": "Heavy orchestral impact, deep resonant brass hold, dead silence",
        "page": 14,
        "duration": "5",
    },

    # --- BLOCK 5: The Warning From Tomorrow ---
    {
        "block": 5,
        "beat": 1,
        "time": "0s-1.5s",
        "title": "The Flaming Eagle Strikes",
        "cast": "@Kang Jin-Hoo @Spirit Shaman",
        "desc": "Supernatural reality shift: the apartment interior dissolves into blazing golden-pink fire and ash as a colossal radiant Spirit Eagle descends with incandescent flaming wings above Jin-Hoo.",
        "camera": "Dynamic upward rotating tilt around Jin-Hoo, 24mm wide angle lens",
        "lighting": "Blazing molten firelight casting deep orange-gold reflections across Jin-Hoo",
        "vo": '(Kang Jin-Hoo): "(internal gasp, trembling) ...It\'s back! The flaming eagle of tomorrow!"',
        "sfx": "Roaring fire vortex, rushing sacred wind, distant eagle cry",
        "page": 15,
        "duration": "5",
    },
    {
        "block": 5,
        "beat": 2,
        "time": "1.5s-3s",
        "title": "The Burning Inscription",
        "cast": "@Spirit Shaman",
        "desc": "Across the fiery smoke within Jin-Hoo\'s vision, burning crimson embers ignite in midair spelling out \'MOUNTAINHILL EXCHANGE\' followed by a shattered padlock and glowing words \'CRITICAL FAILURE / BANKRUPTCY\'.",
        "camera": "Tracking shot sweeping across burning molten typography in midair, 50mm lens",
        "lighting": "Intense crimson backlighting, floating glowing fire embers",
        "vo": '(Spirit Shaman): "(haunting, reverberating spectral warning) The corporate tower you place your trust in... will crumble into ash before sundown."',
        "sfx": "Searing metal hiss, explosive ember sparks, ominous low sub-bass drone",
        "page": 16,
        "duration": "5",
    },
    {
        "block": 5,
        "beat": 3,
        "time": "3s-4.5s",
        "title": "The Desperate Collar Grab",
        "cast": "@Kang Jin-Hoo @Oh Taek-Gyu",
        "desc": "The vision snaps violently back to reality. Jin-Hoo stumbles forward, panting heavily with sweat dripping down his face, grabbing Taek-Gyu\'s hoodie collar with fierce life-or-death intensity.",
        "camera": "Sudden crash cut to medium tight profile, intense handheld shake, 35mm lens",
        "lighting": "Harsh apartment daylight highlighting Jin-Hoo\'s pale, desperate face",
        "vo": '(Kang Jin-Hoo): "(panting, desperate grip) Taek-Gyu! Which exchange holds our cryptocurrency assets right now?! Tell me!"',
        "sfx": "Heavy panting, violent fabric grab rustle, sharp intake of breath",
        "page": 17,
        "duration": "5",
    },
    {
        "block": 5,
        "beat": 4,
        "time": "4.5s-6s",
        "title": "Mountainhill Exchange Named",
        "cast": "@Oh Taek-Gyu",
        "desc": "Taek-Gyu blinks in sheer terror at Jin-Hoo\'s ferocious expression, stammering with wide eyes as he holds his phone defensively against his chest.",
        "camera": "Tight close-up of Taek-Gyu\'s sweating face, 50mm lens",
        "lighting": "Natural daylight reflecting in his fogged glasses",
        "vo": '(Oh Taek-Gyu): "(stammering, confused, scared) M-Mountainhill Exchange... the biggest, most trusted platform in Korea. Why, Jin-Hoo?!"',
        "sfx": "Subtle clock ticking underneath like a countdown timer",
        "page": 17,
        "duration": "5",
    },
    {
        "block": 5,
        "beat": 5,
        "time": "6s-8s",
        "title": "The Table Slam Command",
        "cast": "@Kang Jin-Hoo",
        "desc": "Jin-Hoo slams his palm flat onto the wooden coffee table, towering over Taek-Gyu with blazing authority, his right eye reflecting a lingering phantom golden spark.",
        "camera": "Low-angle dramatic tilt up on Jin-Hoo commanding the room, 35mm lens",
        "lighting": "High-contrast shadow cutting across Jin-Hoo\'s determined jawline",
        "vo": '(Kang Jin-Hoo): "(authoritative, commanding roar) Liquidate everything immediately! Sell every single Bantcoin before noon!"',
        "sfx": "Heavy palm slam on wooden table, deep bass resonance",
        "page": 18,
        "duration": "5",
    },
    {
        "block": 5,
        "beat": 6,
        "time": "8s-10s",
        "title": "The Agonizing Countdown Freeze",
        "cast": "@Oh Taek-Gyu @Kang Jin-Hoo",
        "desc": "Taek-Gyu stares in agonizing hesitation with his thumb trembling millimeters above the sell button on screen, while Jin-Hoo glares down with deadly certainty, locking into a frozen stand-off.",
        "camera": "Split-focus two-shot: trembling thumb over screen in foreground, Jin-Hoo\'s cold face in background",
        "lighting": "Dramatic split lighting, tense shadows across the table",
        "vo": '(Kang Jin-Hoo): "(cold, deadly serious whisper) Put your trust in me... wait another hour and we lose everything we just found." · END ON COMPLETE FREEZE FRAME.',
        "sfx": "Ticking clock abruptly stops, heavy dark cello sustain into silence",
        "page": 18,
        "duration": "5",
    },

    # --- BLOCK 6: The Future Is Real ---
    {
        "block": 6,
        "beat": 1,
        "time": "0s-1.5s",
        "title": "The Sell Execution",
        "cast": "@Oh Taek-Gyu",
        "desc": "Macro close-up of Taek-Gyu\'s sweating thumb slamming down onto a glowing blue confirmation button on the smartphone screen. A clean green confirmation banner flashes: \'SELL ORDER EXECUTED — CASH TRANSFERRED\'.",
        "camera": "Macro close-up on glass screen tap with rapid smooth pull-back, 100mm lens",
        "lighting": "Bright green screen flash illuminating Taek-Gyu\'s trembling fingers",
        "vo": '(Oh Taek-Gyu): "(gasping, nervous exhales) It\'s done! The sell order cleared and the cash hit our bank... but Jin-Hoo, are you positive about this?"',
        "sfx": "Digital transaction confirmation chime, heavy nervous exhale",
        "page": 19,
        "duration": "5",
    },
    {
        "block": 6,
        "beat": 2,
        "time": "1.5s-3s",
        "title": "The 502 Bad Gateway Crash",
        "cast": "@Oh Taek-Gyu",
        "desc": "Thirty seconds later: the phone screen flickers violently with red error bars, flashing an abrupt error pop-up: \'502 BAD GATEWAY — MOUNTAINHILL SERVERS UNREACHABLE\'. Taek-Gyu stares with horror.",
        "camera": "Extreme macro zoom on phone screen displaying red flashing error banner, 85mm lens",
        "lighting": "Pulsing crimson error glow washing across Taek-Gyu\'s horrified face",
        "vo": '(Oh Taek-Gyu): "(voice trembling, eyes widening in panic) W-Wait... the app just crashed. 502 Bad Gateway?! Mountainhill\'s entire server network just went dead?!"',
        "sfx": "Harsh digital error glitch buzz, rising alarm tone",
        "page": 20,
        "duration": "5",
    },
    {
        "block": 6,
        "beat": 3,
        "time": "3s-4.5s",
        "title": "Breaking News Broadcast",
        "cast": "@Oh Taek-Gyu",
        "desc": "Taek-Gyu frantically spins around to his laptop displaying a live news stream: a red breaking news banner scrolls across showing police cars outside Mountainhill headquarters: \'CEO FLEES COUNTRY — EXCHANGE SUSPENDED\'.",
        "camera": "Fast whip pan from phone to flickering laptop screen, 35mm lens",
        "lighting": "Flickering cool laptop screen glow in dark apartment",
        "vo": '(News Anchor on Laptop): "(urgent breaking news report) Breaking news: South Korea\'s largest crypto exchange has abruptly collapsed amid allegations of massive insolvency and executive flight!"',
        "sfx": "Urgent television breaking news siren fanfare, news anchor audio filter",
        "page": 21,
        "duration": "5",
    },
    {
        "block": 6,
        "beat": 4,
        "time": "4.5s-6s",
        "title": "The Awe of Prophecy",
        "cast": "@Oh Taek-Gyu @Kang Jin-Hoo",
        "desc": "Taek-Gyu slowly turns around from the laptop to face Jin-Hoo standing in the apartment center. Taek-Gyu\'s face is pale white, shaking uncontrollably in absolute reverence and terror.",
        "camera": "Slow dramatic low-angle dolly push-in toward Jin-Hoo past Taek-Gyu\'s trembling shoulder, 50mm lens",
        "lighting": "Rich natural chiaroscuro shadows cutting across the small room",
        "vo": '(Oh Taek-Gyu): "(shaking uncontrollably, breathless awe) You foresaw it... you knew this collapse would happen before anyone else. Who on earth are you, Jin-Hoo?!"',
        "sfx": "Deep haunting sub-bass swell, muffled ambient room tone",
        "page": 22,
        "duration": "5",
    },
    {
        "block": 6,
        "beat": 5,
        "time": "6s-8s",
        "title": "The Quiet Confession",
        "cast": "@Kang Jin-Hoo",
        "desc": "Close-up of Kang Jin-Hoo turning his head slowly toward his friend, his expression completely composed, serene, and terrifyingly calm under the morning sunbeam.",
        "camera": "Tight cinematic portrait push-in, 85mm prime lens with rich natural shadows",
        "lighting": "Warm morning light illuminating one half of Jin-Hoo\'s face, deep shadow on the other",
        "vo": '(Kang Jin-Hoo): "(calm, deep, prophetic whisper) I told you earlier, Taek-Gyu... this was never just a lucky guess."',
        "sfx": "Subtle mystical golden chime, deep heartbeat pulse",
        "page": 22,
        "duration": "5",
    },
    {
        "block": 6,
        "beat": 6,
        "time": "8s-10s",
        "title": "The Golden Eye Cliffhanger Freeze",
        "cast": "@Kang Jin-Hoo",
        "desc": "Jin-Hoo steps forward, his right eye igniting with a brilliant golden supernatural spark. He smiles with chilling supreme ambition directly into the camera, locking into a final heroic freeze frame.",
        "camera": "Slow hero push-in directly into Jin-Hoo\'s golden gleaming eye, settling into locked hold",
        "lighting": "Golden mystical rim light igniting around his black hair, background fading to dark contrast",
        "vo": '(Kang Jin-Hoo): "(cold, chilling, triumphant delivery) I see the future. And this is merely the opening move." · END ON COMPLETE FREEZE FRAME: Jin-Hoo locks his golden eye onto the lens, motionless.',
        "sfx": "Massive cinematic bass drop, dramatic orchestral hit, sudden hard cut to silence",
        "page": 23,
        "duration": "5",
    },
]


def format_frame_prompt(frame: dict) -> str:
    """Constructs a clean, single-frame 2D manhwa prompt for Google Flow."""
    cast_prefix = frame["cast"].strip()
    return f"""{cast_prefix}
{MANHUA_STYLE_DIRECTIVE}

[Shot Title]: {frame['title']} ({frame['time']})
[Subject & Visual Action]: {frame['desc']}
[Camera Kinematics]: {frame['camera']}
[Lighting & Atmosphere]: {frame['lighting']}
[Voiceover Script]: {frame['vo']}
[Sound Effects]: {frame['sfx']}
"""


def format_continuous_10s_prompt(block_num: int, frames_in_block: list) -> str:
    """Constructs a single continuous 10-second 2D manhwa scene prompt (no comic cuts)."""
    cast_set = set()
    for f in frames_in_block:
        for c in f["cast"].split():
            if c.startswith("@"):
                cast_set.add(c)
    cast_prefix = " ".join(sorted(cast_set))

    title = frames_in_block[0]["title"]
    actions = " Then, ".join(f["desc"] for f in frames_in_block[:4])
    last_beat = frames_in_block[-1]

    return f"""{cast_prefix}
{MANHUA_STYLE_DIRECTIVE}

[Scene Concept]: Single continuous 10-second 2D manhwa animation sequence for Block {block_num}.
One continuous camera movement through the environment. Smooth cinematic camera tracking, no comic borders, no split screen, no multi-panel grids.

[Continuous Scene Action]: {actions}. The sequence culminates with: {last_beat['desc']}
[Camera Direction]: Continuous fluid 10-second camera progression starting wide and tracking smoothly into a dramatic portrait, locking into a clean freeze frame at 10s.
[Dialogue & Voiceover]: {last_beat['vo']}
"""


def crop_clean_panels():
    """Extract clean 9:16 crops from original webtoon pages for reference."""
    print("[CROPS] Generating clean, borderless 9:16 reference images from original manhwa...")
    for f in FRAMES_DATA:
        p_num = f["page"]
        page_path = IMAGES_DIR / f"page_{p_num:03d}.webp"
        out_crop = CROPS_DIR / f"b{f['block']:02d}_beat{f['beat']}_{f['title'].lower().replace(' ', '_')[:25]}.png"

        if out_crop.exists():
            continue

        if not page_path.exists():
            continue

        try:
            im = Image.open(page_path)
            w, h = im.size
            # Webtoon strips are very tall (e.g. 800x12000). Extract an appropriate 9:16 vertical crop.
            crop_h = int(w * (16 / 9))
            # Offset down based on beat position
            step = min((h - crop_h) // 6, crop_h) if h > crop_h else 0
            offset_y = min((f["beat"] - 1) * step, max(0, h - crop_h))

            box = (0, offset_y, w, min(h, offset_y + crop_h))
            cropped = im.crop(box)
            cropped.save(out_crop, "PNG")
            print(f"  [OK] Cropped: {out_crop.name}")
        except Exception as e:
            print(f"  [WARN] Failed to crop {page_path.name}: {e}")


def main():
    crop_clean_panels()

    # 1. Generate flow_frame_by_frame_queue.csv (All 36 individual cuts)
    fbf_csv_path = FLOW_DIR / "flow_frame_by_frame_queue.csv"
    with open(fbf_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()

        for frame in FRAMES_DATA:
            prompt = format_frame_prompt(frame)
            writer.writerow({
                "prompt": prompt,
                "description": f"SHOT B{frame['block']} Beat {frame['beat']} — {frame['title']} ({frame['time']})",
                "hashtags": HASHTAGS,
                "videoModel": MODEL,
                "videoMode": MODE,
                "videoDurationSeconds": frame["duration"],
                "flowQuantity": "1",
                "videoVoiceReference": frame["cast"].replace("@", "").strip(),
                "flowAspectRatio": ASPECT,
            })

    print(f"\n[OK] Flow Frame-by-Frame CSV (36 Shots): {fbf_csv_path}")

    # 2. Generate per-block frame queues (block1_frames.csv .. block6_frames.csv)
    for b_idx in range(1, 7):
        b_frames = [fr for fr in FRAMES_DATA if fr["block"] == b_idx]
        b_csv_path = FLOW_DIR / f"block{b_idx}_frames_queue.csv"
        with open(b_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
            writer.writeheader()
            for frame in b_frames:
                prompt = format_frame_prompt(frame)
                writer.writerow({
                    "prompt": prompt,
                    "description": f"B{b_idx} Shot {frame['beat']} — {frame['title']} ({frame['time']})",
                    "hashtags": HASHTAGS,
                    "videoModel": MODEL,
                    "videoMode": MODE,
                    "videoDurationSeconds": frame["duration"],
                    "flowQuantity": "1",
                    "videoVoiceReference": frame["cast"].replace("@", "").strip(),
                    "flowAspectRatio": ASPECT,
                })
        print(f"  - Block {b_idx} Frame Queue (6 shots): {b_csv_path.name}")

    # 3. Generate flow_continuous_10s_queue.csv (6 continuous single-camera 10s blocks)
    cont_csv_path = FLOW_DIR / "flow_continuous_10s_queue.csv"
    with open(cont_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()

        for b_idx in range(1, 7):
            b_frames = [fr for fr in FRAMES_DATA if fr["block"] == b_idx]
            prompt = format_continuous_10s_prompt(b_idx, b_frames)
            writer.writerow({
                "prompt": prompt,
                "description": f"CONTINUOUS 10S B{b_idx} — {b_frames[0]['title']}",
                "hashtags": HASHTAGS,
                "videoModel": MODEL,
                "videoMode": MODE,
                "videoDurationSeconds": "10",
                "flowQuantity": "1",
                "videoVoiceReference": b_frames[0]["cast"].replace("@", "").strip(),
                "flowAspectRatio": ASPECT,
            })

    print(f"\n[OK] Flow Continuous 10s Blocks CSV (6 Blocks): {cont_csv_path}")

    # Mirror to e01.csv so default import loads the clean frame-by-frame queue
    default_e01 = FLOW_DIR / "e01.csv"
    with open(default_e01, "w", newline="", encoding="utf-8") as f_out, open(fbf_csv_path, "r", encoding="utf-8") as f_in:
        f_out.write(f_in.read())
    print(f"[OK] Mirrored frame-by-frame queue as default e01.csv for Flow Automator Max.")


if __name__ == "__main__":
    main()
