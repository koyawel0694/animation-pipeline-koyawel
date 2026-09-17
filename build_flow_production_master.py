#!/usr/bin/env python3
"""
build_flow_production_master.py — Master Builder for Google Flow Automator Max (TXT & CSV).
HARDENED VERSION: 100% Policy-Safe (Zero Reputational Risk / Zero Fake News Triggers).

Policy Fix Applied for Google Flow / Veo Filter:
- Root Cause of Error: "Unable to generate videos that might cause reputational risk or misrepresent current events"
  Triggered by: simulated breaking TV news broadcast of corporate crimes ("CEO flees country", "police cars outside headquarters", "crypto exchange insolvency").
- Solution:
  1. Removed all simulated breaking news TV broadcasts, police raids, and real-world-style financial fraud phrasing.
  2. Replaced with stylized in-universe digital network freeze ('NETWORK OFFLINE / SERVERS UNREACHABLE') and fast-scrolling community forum reaction bubbles.
  3. Centered drama strictly on personal character reactions: Taek-Gyu's trembling awe and Jin-Hoo's supernatural golden eye prophecy.
"""

import csv
from pathlib import Path

BASE_DIR = Path("/home/john/manga-reviews/output/the-investor-who-sees-the-future/ch1/flow_queue")
BASE_DIR.mkdir(parents=True, exist_ok=True)

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

BLOCKS = [
    {
        "block_num": 1,
        "title": "The Question That Changes Everything",
        "cast_mentions": ["@Street Reporter", "@Shin Yuri"],
        "description": "VIDEO: E01 B1 — The Question That Changes Everything",
        "voice_ref": "English broadcast male and witty female",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE OPENING",
                "action": "Wide crane shot descending into a bustling modern Seoul pedestrian shopping plaza. Street Reporter (23yo Korean male, tailored charcoal-gray suit, white collared shirt, slim black tie, holding blue wireless broadcast microphone) stands center framing; camera operator in black cap films him in foreground; daylight 5600K ambient city reflections.",
                "camera": "Slow crane down from high angle into eye-level medium-wide tracking, 24mm equivalent lens",
                "lighting": "Bright diffused daylight 5600K, clean urban glass reflections, soft shadows",
                "vo": '(Street Reporter): "(energetic, crisp broadcast projection) Have you ever wondered what you would do if a fortune landed in your hands overnight?"',
                "sfx": "Bustling urban street ambience, footsteps on cobblestones, faint traffic hum",
            },
            {
                "time": "1.5s-3s",
                "label": "THE TURN",
                "action": "Reporter lunges forward enthusiastically toward passersby, extending microphone with an inquisitive challenge smile; background shoppers in modern casual streetwear stop and glance over curiously.",
                "camera": "Smooth dynamic low-angle push-in toward reporter and microphone, 35mm lens",
                "lighting": "Bright daytime sunlight with clean anime cel-shading, crisp highlights on suit",
                "vo": '(Street Reporter): "(dramatic, teasing, eyes wide) What if you suddenly received one hundred million won in cold hard cash?!"',
                "sfx": "Microphone movement whoosh, faint surprised crowd murmur",
            },
            {
                "time": "3s-4.5s",
                "label": "THE REACTION",
                "action": "Cinematic medium shot of Shin Yuri (young Korean woman, wavy honey-blonde hair, beige button-up blouse, delicate gold necklace) walking down the sidewalk; she pauses, rests one manicured finger on her chin, and smiles warmly with effortless intelligence.",
                "camera": "Eye-level medium close-up with soft background anamorphic bokeh, 85mm lens",
                "lighting": "Warm afternoon sunlight, delicate rim light on honey-blonde hair strands",
                "vo": '(Shin Yuri): "(playful, composed chuckle) One hundred million won? That\'s far too little to even put a down payment on an apartment in Seoul..."',
                "sfx": "Gentle city breeze, soft fabric rustle",
            },
            {
                "time": "4.5s-6s",
                "label": "THE ESCALATION",
                "action": "Reporter turns dynamically to interview a young male pedestrian who scratches his head in comical bewilderment while contemplating the sudden wealth.",
                "camera": "Dynamic medium two-shot tracking camera moving subtly between reporter and pedestrian, 50mm lens",
                "lighting": "Midday daylight, storefront glass reflections",
                "vo": '(Street Reporter): "(probing, rapid-fire) A luxury sports car? A startup? Or would you play it safe and stash it away in savings?"',
                "sfx": "Distant bicycle bell, pedestrian chatter",
            },
            {
                "time": "6s-8s",
                "label": "THE HOOK",
                "action": "Tight macro close-up of the reporter\'s sharp gaze and confident grin; he leans directly toward the viewer as if addressing the camera itself.",
                "camera": "Direct frontal slow push-in focusing tightly on eyes and microphone, 85mm prime lens",
                "lighting": "High-contrast street lighting, dramatic shadow under jawline",
                "vo": '(Street Reporter): "(low, conspiratorial, leaning in) Final question... What if you were given the chance to become the richest person in the entire world?"',
                "sfx": "Subtle deep bass swell, street noise fading down",
            },
            {
                "time": "8s-10s",
                "label": "THE CLEVER REBUTTAL — END ON FREEZE FRAME",
                "action": "Shin Yuri crosses her arms, tilts her head with a stunning radiant smile, speaking directly into the microphone; background pedestrians blur into golden daylight bokeh; she finishes her sentence and holds her posture completely still.",
                "camera": "Slow dramatic push-in to tight portrait, locking into a frozen static frame at 10s",
                "lighting": "Golden hour glow accentuating her smile and honey-blonde hair, creamy background blur",
                "vo": '(Shin Yuri): "(sharp, witty smirk) Before I answer that... why don\'t you tell me how to get that rich first?" · END ON COMPLETE FREEZE FRAME: Shin Yuri holds her confident smile and locked gaze through 10s, zero extra movement.',
                "sfx": "Punchy dramatic musical sting, crisp sudden silence with reverberating echo",
            },
        ],
    },
    {
        "block_num": 2,
        "title": "The Man Who Became Richest",
        "cast_mentions": ["@Kang Jin-Hoo", "@Female Interviewer", "@Spirit Shaman"],
        "description": "VIDEO: E01 B2 — The Man Who Became Richest",
        "voice_ref": "English sophisticated male billionaire and female host",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE INTERVIEW",
                "action": "Sleek ultra-modern television broadcast studio with floor-to-ceiling glass windows overlooking Seoul financial high-rises at dusk. Female Interviewer (poised, tailored navy blazer, dark bob) sits opposite Kang Jin-Hoo (23yo Korean male, tailored midnight-navy suit, crisp white shirt, silk tie, tousled jet-black hair); multiple studio broadcast cameras frame them.",
                "camera": "Wide studio tracking dolly glide across glass studio table, 35mm lens",
                "lighting": "Professional TV studio key lighting mixed with cool blue twilight city view",
                "vo": '(Female Interviewer): "(poised, measured respect) You are the youngest person, and the very first Korean, to ever become the richest man in the world."',
                "sfx": "Quiet broadcast studio room hum, soft studio air conditioning tone",
            },
            {
                "time": "1.5s-3s",
                "label": "THE RUMOR",
                "action": "Tight medium close-up of the Female Interviewer leaning forward over cue cards, looking intently into Jin-Hoo\'s calm eyes.",
                "camera": "Slow deliberate push-in on interviewer\'s face, 85mm portrait lens",
                "lighting": "Soft studio beauty lighting, crisp catchlights in her dark eyes",
                "vo": '(Female Interviewer): "(low, intriguing tone) There are persistent rumors surrounding you... that you possess clairvoyance. That you can see the future."',
                "sfx": "Soft rustle of cue card paper, tense silence",
            },
            {
                "time": "3s-4.5s",
                "label": "THE DENIAL",
                "action": "Close-up of Kang Jin-Hoo; he raises his left hand with a calm, gentle dismissive wave, smiling softly with absolute composure.",
                "camera": "Subtle low-angle push-in on Jin-Hoo\'s composed expression, 50mm lens",
                "lighting": "Cool evening city light rimming his tousled black hair, warm studio key on cheek",
                "vo": '(Kang Jin-Hoo): "(calm, smooth, gentle chuckle) Seeing the future? There\'s no such thing. I\'m just an ordinary investor who trusts his timing."',
                "sfx": "Faint low sub-drone pulsing beneath the audio",
            },
            {
                "time": "4.5s-6s",
                "label": "THE GOLDEN EYE",
                "action": "Extreme macro close-up of Kang Jin-Hoo\'s right eye; his pupil dilates as a supernatural radiant amber-gold iris pattern ignites with mystical circuit rings; the studio lights around him suddenly shift into dark emerald shadows.",
                "camera": "Crash zoom into iris reflection, cinematic lens flare, 100mm macro lens",
                "lighting": "Studio light dims into dark emerald shadow, golden iris illuminates his brow",
                "vo": '(Kang Jin-Hoo): "(internal voice, breathless whisper) ...My eye. The golden glow is awakening again."',
                "sfx": "Ethereal high-frequency shimmer, deep mystical resonance pulse",
            },
            {
                "time": "6s-8s",
                "label": "THE APPARITION",
                "action": "Surreal supernatural vision overlaying the television studio: behind the frozen studio crew, the ghostly Spirit Shaman in ancient ceremonial green and gold silk robes materializes in emerald mist, while a colossal radiant bald eagle with incandescent flaming wings ascends with a silent screech.",
                "camera": "High-angle dynamic tilt down looking over the spirit eagle\'s blazing wingspan, 24mm wide angle",
                "lighting": "Blazing golden-pink flame aura contrasting mystical emerald green mist",
                "vo": '(Spirit Shaman): "(ancient, dual-layered spectral voice) You perceive the threads of destiny... but do you possess the courage to reshape them?"',
                "sfx": "Rushing supernatural wind vortex, crackling sacred fire, distant eagle cry",
            },
            {
                "time": "8s-10s",
                "label": "THE COMPOSURE — END ON FREEZE FRAME",
                "action": "Cut back to reality: Kang Jin-Hoo sits upright under the bright studio keylights, the golden glow in his eye fading back to piercing dark obsidian; he offers an enigmatic smirk to the interviewer, completely unfazed; studio crew continues filming.",
                "camera": "Locked eye-level medium close-up, dramatic split lighting",
                "lighting": "Crisp studio keylight, soft city bokeh behind",
                "vo": '(Kang Jin-Hoo): "(enigmatic, quiet confidence) ...I\'m just an ordinary man who knows when to place the winning bet." · END ON A COMPLETE FREEZE FRAME: Kang Jin-Hoo holds his locked smirk and unwavering gaze into the lens through 10s.',
                "sfx": "Heavy orchestral impact, deep heartbeat thump, silence",
            },
        ],
    },
    {
        "block_num": 3,
        "title": "Before the Fortune",
        "cast_mentions": ["@Kang Jin-Hoo", "@Oh Taek-Gyu"],
        "description": "VIDEO: E01 B3 — Before the Fortune",
        "voice_ref": "Young English male veteran and animated best friend",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE WAKING",
                "action": "Flashback: cramped semi-basement apartment bedroom with worn floral wallpaper and morning sunlight filtering through high frosted barred street windows; 23yo Kang Jin-Hoo wearing a plain cream crewneck sweater sits up on his floor mattress, rubbing his temple groggily.",
                "camera": "Low-angle establishing push-in across scattered moving boxes and worn linoleum, 28mm lens",
                "lighting": "Soft pale morning sunlight, gentle dust motes floating in sunbeam",
                "vo": '(Kang Jin-Hoo): "(groggy, heavy sigh) Weeks have passed since my discharge from the army... yet the headache still pounds like an anvil."',
                "sfx": "Distant street traffic outside window, rustle of coarse cotton bedsheets",
            },
            {
                "time": "1.5s-3s",
                "label": "THE DISCHARGE CAP",
                "action": "Close-up of Jin-Hoo picking up his black military discharge service cap with embroidered golden insignia from a dusty shelf; he stares at it quietly, remembering the training accident that gave him the vision.",
                "camera": "Slow macro push-in on military insignia and calloused fingers, 50mm lens",
                "lighting": "Directional morning light casting clean shadows across the cap fabric",
                "vo": '(Kang Jin-Hoo): "(somber whisper, quiet resolve) That bizarre accident during military training... that was where this nightmare began."',
                "sfx": "Soft thud of cap setting down on wood, quiet wall clock tick",
            },
            {
                "time": "3s-4.5s",
                "label": "THE INTRUSION",
                "action": "The apartment door swings open abruptly. Oh Taek-Gyu (23yo Korean male, stocky build, gray zip-up hoodie over white tee, black square-rimmed glasses) barges inside carrying a convenience store plastic bag and a worn notebook, huffing with frantic excitement.",
                "camera": "Medium shot framed from hallway doorway, rapid handheld pan, 35mm lens",
                "lighting": "Hallway daylight silhouetting Taek-Gyu\'s stocky energetic frame",
                "vo": '(Oh Taek-Gyu): "(breathless, shouting excitedly) Jin-Hoo! Are you awake?! You are not going to believe what I just dug up!"',
                "sfx": "Door latch click and swing open, crinkling plastic convenience store bag",
            },
            {
                "time": "4.5s-6s",
                "label": "THE SPREAD",
                "action": "Taek-Gyu drops onto the low wooden coffee table, kicking aside old newspapers, spreading out an old black USB flash drive, crumpled notebook papers with alphanumeric codes, and a phone with an abstract trading chart.",
                "camera": "Overhead high-angle view looking down at table items, 35mm lens",
                "lighting": "Warm interior daylight, clean cell shading on table items",
                "vo": '(Oh Taek-Gyu): "(rapid-fire manic chatter) Remember that Bantcoin we bought back in college before you enlisted? The one everyone mocked us for touching?!"',
                "sfx": "Plastic USB drive clatter on wood, paper rustling aggressively",
            },
            {
                "time": "6s-8s",
                "label": "THE KEY",
                "action": "Medium close-up of Taek-Gyu leaning across the table, thrusting the small black USB drive in front of Jin-Hoo\'s face, his glasses catching window light.",
                "camera": "Tight dynamic over-the-shoulder push-in toward USB drive in palm, 50mm lens",
                "lighting": "Bright morning light reflecting on glasses, joyful anime cel-shading",
                "vo": '(Oh Taek-Gyu): "(triumphant, conspiratorial whisper) I recovered the private encryption key to our forgotten wallet. Jin-Hoo... our account is still alive!"',
                "sfx": "Metallic key clink, subtle low-frequency bass swell",
            },
            {
                "time": "8s-10s",
                "label": "THE REALIZATION — END ON FREEZE FRAME",
                "action": "Jin-Hoo stares at the USB drive in Taek-Gyu\'s palm; his eyes widen with sudden realization as the gravity of the forgotten asset sinks in; Taek-Gyu grins excitedly beside him; daylight streams across their frozen forms.",
                "camera": "Locked frontal medium two-shot with high-contrast morning light",
                "lighting": "Clean morning sunbeams highlighting their faces and table",
                "vo": '(Kang Jin-Hoo): "(stunned, heart dropping) ...Bantcoin? Exactly how many coins did we purchase back then?" · END ON A COMPLETE FREEZE FRAME: Jin-Hoo stares motionless at the key while Taek-Gyu freezes mid-laugh through 10s.',
                "sfx": "Sharp dramatic musical sting, sudden silence with ringing reverb",
            },
        ],
    },
    {
        "block_num": 4,
        "title": "Thirteen Point Five Billion Won",
        "cast_mentions": ["@Kang Jin-Hoo", "@Oh Taek-Gyu"],
        "description": "VIDEO: E01 B4 — Thirteen Point Five Billion Won",
        "voice_ref": "Two young English male voices realizing sudden fortune",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE LOGIN",
                "action": "Medium shot over Jin-Hoo\'s shoulder: Taek-Gyu holds his smartphone horizontally over the wooden table, fingers typing an abstract pin on a dark cryptocurrency exchange interface with glowing cyan numbers.",
                "camera": "Macro over-the-shoulder Dutch angle tilt, 50mm lens",
                "lighting": "Cyan screen glow casting soft blue light on their hands and faces",
                "vo": '(Oh Taek-Gyu): "(nervous, gulping) Hold on... the exchange wallet is decrypting. Let\'s see what crumbs are left."',
                "sfx": "Digital interface confirmation chime, rapid screen tap clicks",
            },
            {
                "time": "1.5s-3s",
                "label": "THE NUMBERS",
                "action": "Close-up of Taek-Gyu\'s face illuminated by bright blue screen glow; his jaw hangs slack, round eyes wide in paralyzing shock as color drains from his cheeks.",
                "camera": "Slow crash push-in on Taek-Gyu\'s wide stunned eyes behind glasses, 85mm lens",
                "lighting": "Intense cool blue screen reflection on his glasses and forehead",
                "vo": '(Oh Taek-Gyu): "(trembling whisper, voice cracking) Jin-Hoo... are my eyes completely playing tricks on me? Or is this screen malfunctioning?!"',
                "sfx": "High-pitched ringing tinnitus tone, muted room ambiance",
            },
            {
                "time": "3s-4.5s",
                "label": "THE CALCULATION",
                "action": "Jin-Hoo leans forward over the table, gripping Taek-Gyu\'s wrist to steady the shaking phone; Jin-Hoo\'s brows furrow tightly as he rapidly calculates the conversion rates in his head.",
                "camera": "Medium tight two-shot, dynamic whip pan from shaking hands to Jin-Hoo\'s intense face, 35mm lens",
                "lighting": "Dramatic split light, one side bathed in blue screen glow, other in morning sun",
                "vo": '(Kang Jin-Hoo): "(intense, calculating under breath) Three thousand coins... multiplied by the current real-time market spot price..."',
                "sfx": "Rapid heartbeat pulse, rising sub-bass swell",
            },
            {
                "time": "4.5s-6s",
                "label": "THE BOMBSHELL",
                "action": "Taek-Gyu leaps to his feet, knocking his plastic chair backward onto the floor, clutching his head with both hands in hysterical manic disbelief.",
                "camera": "Low-angle wide shot capturing Taek-Gyu standing with arms raised, 24mm wide lens",
                "lighting": "Bright apartment interior, dynamic anime speed lines radiating outward",
                "vo": '(Oh Taek-Gyu): "(screaming in manic disbelief) THIRTEEN POINT FIVE BILLION! 13.5 Billion Won! We are multi-billionaire moguls, Jin-Hoo!"',
                "sfx": "Plastic chair clattering to the floor, Taek-Gyu yelling echoes",
            },
            {
                "time": "6s-8s",
                "label": "THE PLEA",
                "action": "Taek-Gyu drops back to his knees beside Jin-Hoo, aggressively shaking Jin-Hoo\'s shoulders with an absurd, tearful comedic smile, begging him to confirm it\'s real.",
                "camera": "Medium close-up, energetic comedic handheld shake, 50mm lens",
                "lighting": "Warm morning apartment light, comical tear streaks on Taek-Gyu\'s cheeks",
                "vo": '(Oh Taek-Gyu): "(laughing and crying simultaneously) Tell me I\'m not dreaming! Slap me across the face, Jin-Hoo! Is this actually real?!"',
                "sfx": "Fabric grabbing rustle, heavy frantic breathing and laughter",
            },
            {
                "time": "8s-10s",
                "label": "THE GAZE UPWARD — END ON FREEZE FRAME",
                "action": "Jin-Hoo pulls away gently, looking down at the glowing phone screen and then up toward the ceiling as if peering through the roof into the city; his eyes turn cold, solemn, and intensely focused.",
                "camera": "Slow dramatic low-angle push-in on Jin-Hoo\'s unblinking profile",
                "lighting": "Moody chiaroscuro shadow cutting across Jin-Hoo\'s jawline",
                "vo": '(Kang Jin-Hoo): "(deep, cold, resolute) ...This is no dream. But if we aren\'t careful, a fortune like this can vanish in a single breath." · END ON COMPLETE FREEZE FRAME.',
                "sfx": "Heavy orchestral impact, deep resonant brass hold, dead silence",
            },
        ],
    },
    {
        "block_num": 5,
        "title": "The Warning From Tomorrow",
        "cast_mentions": ["@Kang Jin-Hoo", "@Oh Taek-Gyu", "@Spirit Shaman"],
        "description": "VIDEO: E01 B5 — The Warning From Tomorrow",
        "voice_ref": "Young English visionary and spiritual omen",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE VISION BURST",
                "action": "Supernatural reality shift: the apartment interior dissolves into blazing golden-pink fire and ash as a colossal radiant Spirit Eagle descends with incandescent flaming wings above Jin-Hoo.",
                "camera": "Dynamic upward rotating tilt around Jin-Hoo, 24mm wide angle lens",
                "lighting": "Blazing molten firelight casting deep orange-gold reflections across Jin-Hoo",
                "vo": '(Kang Jin-Hoo): "(internal gasp, trembling) ...It\'s back! The flaming eagle of tomorrow!"',
                "sfx": "Roaring fire vortex, rushing sacred wind, distant eagle cry",
            },
            {
                "time": "1.5s-3s",
                "label": "THE BURNING OMEN",
                "action": "Across the fiery smoke within Jin-Hoo\'s trance, burning crimson embers ignite in midair forming glowing abstract geometric symbols of a shattered exchange vault and the mystical warning words: 'SYSTEM COLLAPSE / IMMINENT DOWNTIME'.",
                "camera": "Tracking shot sweeping across burning molten symbols in midair, 50mm lens",
                "lighting": "Intense crimson backlighting, floating glowing fire embers",
                "vo": '(Spirit Shaman): "(haunting, reverberating spectral warning) The fortress you placed your faith in... will dissolve into shadows before the sun sets."',
                "sfx": "Searing metal hiss, explosive ember sparks, ominous low sub-bass drone",
            },
            {
                "time": "3s-4.5s",
                "label": "THE INQUIRY",
                "action": "The vision snaps violently back to reality. Jin-Hoo stumbles forward, panting heavily with sweat dripping down his face, grabbing Taek-Gyu\'s hoodie collar with fierce life-or-death intensity.",
                "camera": "Sudden crash cut to medium tight profile, intense handheld shake, 35mm lens",
                "lighting": "Harsh apartment daylight highlighting Jin-Hoo\'s pale, desperate face",
                "vo": '(Kang Jin-Hoo): "(panting, desperate grip) Taek-Gyu! Which digital platform holds our assets right now?! Tell me!"',
                "sfx": "Heavy panting, violent fabric grab rustle, sharp intake of breath",
            },
            {
                "time": "4.5s-6s",
                "label": "THE ANSWER",
                "action": "Taek-Gyu blinks in sheer terror at Jin-Hoo\'s ferocious expression, stammering with wide eyes as he holds his phone defensively against his chest.",
                "camera": "Tight close-up of Taek-Gyu\'s sweating face, 50mm lens",
                "lighting": "Natural daylight reflecting in his fogged glasses",
                "vo": '(Oh Taek-Gyu): "(stammering, confused, scared) Mountainhill... the largest, most secure platform in the region. Why, Jin-Hoo?!"',
                "sfx": "Subtle clock ticking underneath like a countdown timer",
            },
            {
                "time": "6s-8s",
                "label": "THE COMMAND",
                "action": "Jin-Hoo slams his palm flat onto the wooden coffee table, towering over Taek-Gyu with blazing authority, his right eye reflecting a lingering phantom golden spark.",
                "camera": "Low-angle dramatic tilt up on Jin-Hoo commanding the room, 35mm lens",
                "lighting": "High-contrast shadow cutting across Jin-Hoo\'s determined jawline",
                "vo": '(Kang Jin-Hoo): "(authoritative, commanding roar) Liquidate everything immediately! Withdraw every single coin before noon!"',
                "sfx": "Heavy palm slam on wooden table, deep bass resonance",
            },
            {
                "time": "8s-10s",
                "label": "THE IMPOSSIBLE DEMAND — END ON FREEZE FRAME",
                "action": "Taek-Gyu stares in agonizing hesitation with his thumb trembling millimeters above the confirm button on screen, while Jin-Hoo glares down with deadly certainty, locking into a frozen stand-off.",
                "camera": "Split-focus two-shot: trembling thumb over screen in foreground, Jin-Hoo\'s cold face in background",
                "lighting": "Dramatic split lighting, tense shadows across the table",
                "vo": '(Kang Jin-Hoo): "(cold, deadly serious whisper) Put your trust in me... wait another hour and everything we found is gone." · END ON COMPLETE FREEZE FRAME.',
                "sfx": "Ticking clock abruptly stops, heavy dark cello sustain into silence",
            },
        ],
    },
    {
        "block_num": 6,
        "title": "The Future Is Real",
        "cast_mentions": ["@Kang Jin-Hoo", "@Oh Taek-Gyu"],
        "description": "VIDEO: E01 B6 — The Future Is Real",
        "voice_ref": "Stunned young men witnessing prophetic fulfillment",
        "beats": [
            {
                "time": "0s-1.5s",
                "label": "THE CONFIRMATION",
                "action": "Macro close-up of Taek-Gyu\'s sweating thumb pressing firmly onto a glowing blue confirmation button on the smartphone screen. A clean green notification banner appears: \'WITHDRAWAL COMPLETE — FULL BALANCE TRANSFERRED TO BANK\'.",
                "camera": "Macro close-up on glass screen tap with rapid smooth pull-back, 100mm lens",
                "lighting": "Bright green screen flash illuminating Taek-Gyu\'s trembling fingers",
                "vo": '(Oh Taek-Gyu): "(gasping, nervous exhales) It\'s through! The full cash balance just cleared into our personal bank accounts... but Jin-Hoo, are you positive about this?"',
                "sfx": "Digital transaction confirmation chime, heavy nervous exhale",
            },
            {
                "time": "1.5s-3s",
                "label": "THE SYSTEM BLACKOUT",
                "action": "Suddenly, thirty seconds later: the phone screen displays a harsh red network disconnect symbol with an abrupt error code: \'502 GATEWAY ERROR — SERVER CLUSTER OFFLINE — ACCESS RESTRICTED\'. Taek-Gyu gasps in shock.",
                "camera": "Extreme macro zoom on phone screen displaying red flashing error symbol, 85mm lens",
                "lighting": "Pulsing crimson error glow washing across Taek-Gyu\'s horrified face",
                "vo": '(Oh Taek-Gyu): "(voice trembling, eyes widening in panic) W-Wait... the entire network just went black! The whole platform servers completely shut down?!"',
                "sfx": "Harsh digital error glitch buzz, rising alarm tone",
            },
            {
                "time": "3s-4.5s",
                "label": "THE FORUM PANIC",
                "action": "Taek-Gyu frantically spins around to his laptop where online community discussion boards scroll at dizzying speed with thousands of frantic red user alerts and exclamation icons as users report frozen accounts.",
                "camera": "Fast whip pan from phone to chaotic scrolling laptop screen, 35mm lens",
                "lighting": "Rapidly flickering laptop screen glow reflecting on Taek-Gyu\'s wide glasses",
                "vo": '(Oh Taek-Gyu): "(frantic, reading rapid comments) Millions of users locked out... trading is halted indefinitely across the entire network!"',
                "sfx": "Rapid cascade of digital ping notifications, low sub-bass rumble",
            },
            {
                "time": "4.5s-6s",
                "label": "THE AWE OF PROPHECY",
                "action": "Taek-Gyu slowly turns around from the laptop to face Jin-Hoo standing in the quiet apartment. Taek-Gyu\'s face is pale white, shaking uncontrollably in absolute reverence and terror, realizing his friend saw tomorrow.",
                "camera": "Slow dramatic low-angle dolly push-in toward Jin-Hoo past Taek-Gyu\'s trembling shoulder, 50mm lens",
                "lighting": "Rich natural chiaroscuro shadows cutting across the small room",
                "vo": '(Oh Taek-Gyu): "(shaking uncontrollably, breathless awe) You foresaw it... you pulled us out minutes before total shutdown. Who on earth are you, Jin-Hoo?!"',
                "sfx": "Deep haunting sub-bass swell, muffled ambient room tone",
            },
            {
                "time": "6s-8s",
                "label": "THE QUIET CONFESSION",
                "action": "Close-up of Kang Jin-Hoo turning his head slowly toward his friend, his expression completely composed, serene, and terrifyingly calm under the morning sunbeam cutting across the room.",
                "camera": "Tight cinematic portrait push-in, 85mm prime lens with rich natural shadows",
                "lighting": "Warm morning light illuminating one half of Jin-Hoo\'s face, deep shadow on the other",
                "vo": '(Kang Jin-Hoo): "(calm, deep, prophetic whisper) I told you earlier, Taek-Gyu... this was never just a lucky guess."',
                "sfx": "Subtle mystical golden chime, deep heartbeat pulse",
            },
            {
                "time": "8s-10s",
                "label": "THE CLIFFHANGER — END ON FREEZE FRAME",
                "action": "Jin-Hoo steps forward, his right eye igniting with a brilliant golden supernatural spark. He smiles with chilling supreme ambition directly into the camera, locking into a final heroic freeze frame.",
                "camera": "Slow hero push-in directly into Jin-Hoo\'s golden gleaming eye, settling into locked hold at 10s",
                "lighting": "Golden mystical rim light igniting around his black hair, background fading to dark contrast",
                "vo": '(Kang Jin-Hoo): "(cold, chilling, triumphant delivery) I see the future. And this is merely the opening move." · END ON COMPLETE FREEZE FRAME: Jin-Hoo locks his golden eye onto the lens, motionless.',
                "sfx": "Massive cinematic bass drop, dramatic orchestral hit, sudden hard cut to silence",
            },
        ],
    },
]


def format_block_prompt(block: dict) -> str:
    """Build the exact 10s multi-beat walkthrough containing all timestamps."""
    mentions = " ".join(block["cast_mentions"])
    header = f'SERYE DRAMA BLOCK — The Investor Who Sees The Future — Block {block["block_num"]} "{block["title"]}" (10s, 6 beats)'
    inputs = (
        f"INPUTS: attached image ingredients = faces of {', '.join(block['cast_mentions'])} only (ref-locked). "
        "Animate strictly following the time-labeled beats below:"
    )

    lines = [mentions, STYLE_HEADER, "", header, inputs, ""]
    for b in block["beats"]:
        line = (
            f'{b["time"]} — {b["label"]}: {b["action"]} · '
            f'CAMERA: {b["camera"]} · LIGHTING: {b["lighting"]} · '
            f'VO: {b["vo"]} · SFX: {b["sfx"]}'
        )
        lines.append(line)
        lines.append("")

    return "\n".join(lines).strip()


def main():
    # 1. Build flow_6_continuous_blocks.txt
    block_prompts = []
    episode_rows = []

    for b in BLOCKS:
        prompt_text = format_block_prompt(b)
        block_prompts.append(prompt_text)

        # Per-block individual txt file
        p_txt = BASE_DIR / f"block{b['block_num']}_prompts.txt"
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

    # Save flow_6_continuous_blocks.txt
    cont_txt_path = BASE_DIR / "flow_6_continuous_blocks.txt"
    with open(cont_txt_path, "w", encoding="utf-8") as f:
        f.write(DELIMITER.join(block_prompts) + "\n")
    print(f"[OK] Hardened 10s Blocks TXT (Policy-Safe): {cont_txt_path}")

    # Save e01.csv
    e01_csv_path = BASE_DIR / "e01.csv"
    with open(e01_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        for r in episode_rows:
            writer.writerow(r)
    print(f"[OK] Hardened e01.csv: {e01_csv_path}")

    # Save flow_continuous_10s_queue.csv
    cont_csv_path = BASE_DIR / "flow_continuous_10s_queue.csv"
    with open(cont_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        for r in episode_rows:
            writer.writerow(r)
    print(f"[OK] Hardened flow_continuous_10s_queue.csv: {cont_csv_path}")


if __name__ == "__main__":
    main()
