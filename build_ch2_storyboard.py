#!/usr/bin/env python3
import json
import html
from pathlib import Path

OUT_DIR = Path('/home/john/manga-reviews/output/the-investor-who-sees-the-future/ch2')

BLOCKS = [
    {
        "block_title": "The Mortar Range Drill",
        "duration_sec": 10,
        "format": "9:16 vertical video",
        "source_pages": ["page_001.webp", "page_002.webp"],
        "beats": [
            {
                "timestamp": "0s-1.5s",
                "label": "THE PROLOGUE",
                "page_number": 1,
                "page_file": "page_001.webp",
                "scene_title": "Mortar Firing Range Flashback",
                "action": "Flashback to one year ago: high-angle panoramic establishing shot over a sun-baked South Korean army artillery firing range nestled between rugged forested mountains. A battery of 81mm mortar tubes stands anchored into packed earth trenches with green ammunition crates.",
                "camera": "Slow crane down through heat distortion haze into mortar firing line, 28mm lens",
                "vo": '(Narrator): "(solemn, reflective documentary cadence) One year ago... Mortar Firing Range, Infantry Regiment. Where the impossible began."',
                "sfx": "Distant thundering artillery concussions echoing across hills, dry mountain wind",
                "story_flow": "Establishes a flashback set one year prior at a military mortar firing range during a training drill."
            },
            {
                "timestamp": "1.5s-3s",
                "label": "THE REPRIMAND",
                "page_number": 1,
                "page_file": "page_001.webp",
                "scene_title": "Senior Soldier Scolds Kang Jin-hoo",
                "action": "The veteran Drill Sergeant in full combat gear and camouflage helmet steps aggressively into frame, glaring down with hands on hips and shouting furiously at Jin-Hoo.",
                "camera": "Low-angle medium close-up tracking into the sergeant's stern shouting face, 35mm lens",
                "vo": '(Drill Sergeant): "(furious, gravelly military bark) Private Kang Jin-Hoo! Stop daydreaming and lock your eyes forward! Keep your head in the drill!"',
                "sfx": "Heavy combat boots crunching gravel, crisp leather gear creaking",
                "story_flow": "Depicts Kang Jin-hoo getting reprimanded by his superior for being distracted during the field exercise."
            },
            {
                "timestamp": "3s-4.5s",
                "label": "THE DISCIPLINED SALUTE",
                "page_number": 1,
                "page_file": "page_001.webp",
                "scene_title": "Kang Jin-hoo's Disciplined Shout",
                "action": "Private Kang Jin-Hoo snaps to attention, eyes burning with disciplined intensity, chest puffed out, throwing a razor-sharp military salute in pristine soldier form.",
                "camera": "Direct frontal hero eye-level portrait shot, 50mm lens",
                "vo": '(Kang Jin-Hoo): "(disciplined, resonant military shout) Private Kang Jin-Hoo! Understood, Drill Sergeant, Sir!"',
                "sfx": "Sharp uniform fabric snap, disciplined synchronized squad boots shifting",
                "story_flow": "Kang Jin-hoo snaps back to attention, affirming his focus with rigid military obedience."
            },
            {
                "timestamp": "4.5s-6s",
                "label": "THE GOLDEN GLOW",
                "page_number": 1,
                "page_file": "page_001.webp",
                "scene_title": "Mysterious Golden Glow",
                "action": "Jin-Hoo turns his head slightly; up in the mountain forest canopy behind the firing range, a mysterious, ethereal amber-gold light begins to shimmer amidst the pine trees.",
                "camera": "Dutch-angle tilt looking up through the pine branches into the golden radiance, 85mm lens",
                "vo": '(Kang Jin-Hoo): "(internal whisper, bewildered breath) Huh...? What is that golden glow flickering in the canopy...?"',
                "sfx": "Soft unnatural high-frequency harmonic hum, light mountain breeze rustling needles",
                "story_flow": "Kang Jin-hoo's focus drifts again as he notices an abnormal luminescence in the trees."
            },
            {
                "timestamp": "6s-8s",
                "label": "THE GOLDEN EAGLE",
                "page_number": 2,
                "page_file": "page_002.webp",
                "scene_title": "Golden Eagle in the Trees",
                "action": "Perched on a thick pine branch, a majestic raptor enveloped in intense golden mist and crackling amber sparks stares unblinkingly down at Jin-Hoo with piercing supernatural eyes.",
                "camera": "Dramatic slow push-in on the glowing golden eagle, 70mm telephoto lens",
                "vo": '(Kang Jin-Hoo): "(whispering in breathless disbelief) An eagle...? Enveloped in golden light... staring right into me?!"',
                "sfx": "Ethereal mystical pulse, subtle wind chime harmonic resonance",
                "story_flow": "Kang Jin-hoo's attention is captured by an eagle enveloped in an abnormal glowing mist."
            },
            {
                "timestamp": "8s-10s",
                "label": "THE STREAK OVERHEAD",
                "page_number": 2,
                "page_file": "page_002.webp",
                "scene_title": "Eagle Swooping in Golden Lightning",
                "action": "The eagle launches into flight, streaking like a bolt of amber lightning across the open sky directly above the squad. Jin-Hoo recoils backward, eyes wide with adrenaline as the blazing golden arc locks into a complete held freeze frame. End on a complete freeze frame: subject holds final pose, eyes and hands still, no new action.",
                "camera": "Dynamic whip-pan tracking the golden streak overhead, locked static hold through 10s",
                "vo": '(Kang Jin-Hoo): "(alarmed gasp, trembling shock) It\'s swooping down right over our heads! Look out!"',
                "sfx": "Piercing sonic whoosh of rushing wind and thunderous crack; final impact, then silence",
                "story_flow": "The eagle swoops violently, passing directly over the squad in a streak of amber lightning."
            }
        ]
    },
    {
        "block_title": "The Premonition and Explosion",
        "duration_sec": 10,
        "format": "9:16 vertical video",
        "source_pages": ["page_003.webp", "page_004.webp"],
        "beats": [
            {
                "timestamp": "0s-1.5s",
                "label": "THE SQUADMATE DENIAL",
                "page_number": 3,
                "page_file": "page_003.webp",
                "scene_title": "Squadmate's Clueless Denial",
                "action": "Jin-Hoo frantically points upward, but his squadmate looks up at the empty blue sky, blinking blankly and laughing with a bewildered smirk.",
                "camera": "Over-the-shoulder medium reaction two-shot, 35mm lens",
                "vo": '(Squadmate): "(confused chuckle, bewildered) An eagle made of light? There\'s nothing up there, Jin-Hoo! You\'re losing your mind!"',
                "sfx": "Squadmate chuckle, distant clatter of artillery shells in the trench",
                "story_flow": "Confirms that the golden entity was entirely invisible to everyone else in the squad."
            },
            {
                "timestamp": "1.5s-3s",
                "label": "THE GOLDEN HUD",
                "page_number": 3,
                "page_file": "page_003.webp",
                "scene_title": "The Golden Warning Appears",
                "action": "Extreme macro close-up of Jin-Hoo's right eye: glowing golden geometric numerals and warning reticles ignite inside his pupil, outlining the 81mm mortar barrel with flashing red hazard alerts.",
                "camera": "Extreme macro zoom directly into Jin-Hoo's dilating iris, 100mm macro lens",
                "vo": '(Kang Jin-Hoo): "(breathless, terrified whisper) Augmented reality inside my eye...? No... this is a warning from the future!"',
                "sfx": "High-tech digital ping, deep resonant heartbeat thump",
                "story_flow": "A supernatural golden HUD materializes in Jin-hoo's vision, warning of an imminent hazard."
            },
            {
                "timestamp": "3s-4.5s",
                "label": "THE MORTAR SHELL",
                "page_number": 4,
                "page_file": "page_004.webp",
                "scene_title": "Loading the Mortar Shell",
                "action": "In slow motion, a soldier loads a heavy 81mm high-explosive mortar shell into the steel muzzle; Jin-Hoo watches the metallic fin slide down the dark bore.",
                "camera": "Slow-motion Dutch low-angle tracking the shell sliding into the muzzle, 50mm lens",
                "vo": '(Narrator): "(grim, tense retrospective cadence) Even now, I can say this without exaggeration: the body moves before the mind can understand."',
                "sfx": "Metallic clank of mortar round sliding down steel barrel, muffled bass heartbeat",
                "story_flow": "Shows the mortar round being loaded into the tube as Jin-hoo urgently realizes the premonition is coming to pass."
            },
            {
                "timestamp": "4.5s-6s",
                "label": "THE FATAL COUNTDOWN",
                "page_number": 4,
                "page_file": "page_004.webp",
                "scene_title": "Primal Chill of Mortal Peril",
                "action": "The golden HUD flashes violently with countdown numbers: 03... 02... 01... The barrel begins to bulge with catastrophic internal pressure as the hair-trigger misfire reaches zero.",
                "camera": "Rapid snap-zoom on the glowing hairline fracture spreading across the steel tube, 85mm lens",
                "vo": '(Kang Jin-Hoo): "(internal scream of absolute mortal terror) The barrel is going to rupture! The shell is jammed in the chamber!"',
                "sfx": "High-frequency metal stress screech, deafening pressure whine",
                "story_flow": "Narrates the primal chill of impending death as Jin-hoo senses the immediate catastrophe."
            },
            {
                "timestamp": "6s-8s",
                "label": "THE DESPERATE DIVE",
                "page_number": 4,
                "page_file": "page_004.webp",
                "scene_title": "Desperate Warning and Dive",
                "action": "Driven by pure instinct, Jin-Hoo launches his entire body forward in a flying tackle, slamming his squadmates down into the dirt embankment.",
                "camera": "Dynamic low tracking shot rushing alongside Jin-Hoo's mid-air dive, 28mm lens",
                "vo": '(Kang Jin-Hoo): "(throat-shredding, frantic scream) GET DOWNNNN! EVERYBODY HIT THE DIRT!!"',
                "sfx": "Roar of wind, heavy tactical bodies crashing violently into the packed earth",
                "story_flow": "Jin-hoo screams a desperate warning and throws himself forward to tackle his squadmates out of danger."
            },
            {
                "timestamp": "8s-10s",
                "label": "THE CATASTROPHIC DETONATION",
                "page_number": 4,
                "page_file": "page_004.webp",
                "scene_title": "Catastrophic Mortar Explosion",
                "action": "The mortar tube detonates in a massive fireball of shrapnel and black smoke. Jin-Hoo shields his squadmate beneath his body as the fiery shockwave bursts overhead, freezing into an iconic hero silhouette. End on a complete freeze frame: subject holds final pose, eyes and hands still, no new action.",
                "camera": "Low-angle dramatic wide shot of the fireball expanding above Jin-Hoo's shielding silhouette, locked static hold through 10s",
                "vo": '(Narrator): "(solemn, thunderous impact) A catastrophic barrel explosion. He shielded his men from certain death... and unlocked a vision of tomorrow."',
                "sfx": "Thunderous explosion boom with ringing ear-tinnitus whine; final impact, then silence",
                "story_flow": "The mortar tube explodes catastrophically, engulfing the scene in fire and flying shrapnel."
            }
        ]
    },
    {
        "block_title": "Twice Means A Superpower",
        "duration_sec": 10,
        "format": "9:16 vertical video",
        "source_pages": ["page_005.webp", "page_006.webp"],
        "beats": [
            {
                "timestamp": "0s-1.5s",
                "label": "THE STUDIO REFLECTION",
                "page_number": 5,
                "page_file": "page_005.webp",
                "scene_title": "Pensive Silence in the Studio",
                "action": "Dissolve from the explosion to present day: Jin-Hoo sits quietly at a wooden desk in a cozy semi-basement Seoul studio, wearing a clean civilian crewneck shirt, his military discharge cap resting nearby.",
                "camera": "Slow push-in past the green military cap onto Jin-Hoo's sharp, contemplative face, 50mm lens",
                "vo": '(Kang Jin-Hoo): "(quiet, pensive murmur) Discharged as an injured veteran. The military doctor called it accident trauma... but I knew what I saw."',
                "sfx": "Gentle distant city traffic, clock ticking softly on the wall",
                "story_flow": "Transitions to the present day in Jin-hoo's residence, showing him quietly reflecting on the incident."
            },
            {
                "timestamp": "1.5s-3s",
                "label": "THE MIRACULOUS SURVIVAL",
                "page_number": 5,
                "page_file": "page_005.webp",
                "scene_title": "Miraculous Survival",
                "action": "Across the room, bespectacled friend Oh Taek-Gyu leans forward on his chair, pushing up his thick black frames with genuine amazement in his eyes.",
                "camera": "Medium shot of Taek-Gyu adjusting his glasses, 35mm lens",
                "vo": '(Oh Taek-Gyu): "(awed, earnest sympathy) You were unbelievably lucky, Jin-Hoo. A direct mortar misfire usually leaves zero survivors. You survived without a scratch!"',
                "sfx": "Chair wooden creak, gentle keyboard key click",
                "story_flow": "Taek-gyu expresses disbelief at Jin-hoo surviving such a deadly training accident."
            },
            {
                "timestamp": "3s-4.5s",
                "label": "TWICE MEANS A SUPERPOWER",
                "page_number": 6,
                "page_file": "page_006.webp",
                "scene_title": "Twice Means a Superpower",
                "action": "Taek-Gyu points a finger decisively into the air, a confident otaku smirk spreading across his round face as he analyzes the pattern.",
                "camera": "Tight medium close-up of Taek-Gyu smirking with raised finger, 50mm lens",
                "vo": '(Oh Taek-Gyu): "(giddy, dramatic deduction) Once is a coincidence. But twice? If you foresaw the mortar explosion AND the Bantcoin crash... that means it\'s a superpower!"',
                "sfx": "Finger tap on table, playful dramatic flourish sound",
                "story_flow": "Taek-gyu rationalizes Jin-hoo's recurring premonitions, arguing that two occurrences elevate it to a superpower."
            },
            {
                "timestamp": "4.5s-6s",
                "label": "JIN-HOO'S SKEPTICISM",
                "page_number": 6,
                "page_file": "page_006.webp",
                "scene_title": "Jin-hoo's Skepticism",
                "action": "Jin-Hoo crosses his arms, looking at Taek-Gyu with a wry, skeptical half-smile, grounded in harsh economic reality.",
                "camera": "Medium profile shot of Jin-Hoo crossing arms and raising an eyebrow, 50mm lens",
                "vo": '(Kang Jin-Hoo): "(dry, grounded amusement) A superpower? Even if you\'re right, Taek-Gyu, how can you accept something so absurd so casually?"',
                "sfx": "Soft rustle of fabric, quiet chuckling breath",
                "story_flow": "Jin-hoo challenges Taek-gyu's readiness to accept supernatural phenomena as everyday reality."
            },
            {
                "timestamp": "6s-8s",
                "label": "OTAKU FORTITUDE",
                "page_number": 6,
                "page_file": "page_006.webp",
                "scene_title": "Otaku Fortitude",
                "action": "Taek-Gyu puffs his chest out proudly, brandishing a limited-edition anime collectible with exaggerated philosophical conviction.",
                "camera": "Low-angle dynamic push-in on Taek-Gyu puffing out his chest, 35mm lens",
                "vo": '(Oh Taek-Gyu): "(boastful, energetic pride) Never underestimate the mental fortitude forged by ten thousand hours of anime and web novels! My brain is built for supernatural events!"',
                "sfx": "Comic heroic chime, swift arm gesture whoosh",
                "story_flow": "Taek-gyu credits his lifelong immersion in fantasy media with his open-minded adaptability."
            },
            {
                "timestamp": "8s-10s",
                "label": "THE STAGGERING SHARE",
                "page_number": 6,
                "page_file": "page_006.webp",
                "scene_title": "The Staggering Share",
                "action": "Jin-Hoo cuts through the banter, placing both hands flat on the wooden table, his dark eyes locking onto Taek-Gyu with razor-sharp intensity as he drops the bombshell amount. End on a complete freeze frame: subject holds final pose, eyes and hands still, no new action.",
                "camera": "Slow, intense push-in toward Jin-Hoo's piercing eyes, locked static hold through 10s",
                "vo": '(Kang Jin-Hoo): "(calm, cold, absolute authority) Enough anime talk. Let\'s get down to practical business. My share: exactly 1.24 billion won."',
                "sfx": "Solid table thud, dramatic low bass drop; final impact, then silence",
                "story_flow": "Jin-hoo drops a monetary bombshell, demanding an exact share of 1.24 billion won."
            }
        ]
    },
    {
        "block_title": "The 1.24 Billion Won Share",
        "duration_sec": 10,
        "format": "9:16 vertical video",
        "source_pages": ["page_007.webp", "page_008.webp"],
        "beats": [
            {
                "timestamp": "0s-1.5s",
                "label": "THE STUNNED SILENCE",
                "page_number": 7,
                "page_file": "page_007.webp",
                "scene_title": "Jin-hoo's Defiant Stare",
                "action": "Taek-Gyu stares blankly in utter disbelief, his jaw dangling open like a broken hinge as the sheer number echoes in the room.",
                "camera": "Deadpan frontal close-up on Taek-Gyu's frozen gaping expression, 85mm lens",
                "vo": '(Oh Taek-Gyu): "(choked, squeaking whisper) O-One point two four... billion won?! What kind of math is that?!"',
                "sfx": "High-pitched comic whistle, stunned silence",
                "story_flow": "Following his sudden demand for 1.24 billion won, Jin-hoo confronts Taek-gyu's stunned silence."
            },
            {
                "timestamp": "1.5s-3s",
                "label": "THE FIGURE HOSTAGE",
                "page_number": 7,
                "page_file": "page_007.webp",
                "scene_title": "Extortion by Fire",
                "action": "Jin-Hoo picks up Taek-Gyu's prized limited-edition anime figurine, holding a lighter beneath it with an icy, menacing smirk while breaking down the account calculations.",
                "camera": "Dynamic two-shot framing Jin-Hoo holding the lighter under the precious collectible, 35mm lens",
                "vo": '(Kang Jin-Hoo): "(sweet, predatory calm) When you liquidated your Lutnia character, you bundled my high-level items too. If my cut doesn\'t land... your waifu burns."',
                "sfx": "Lighter click and gentle hiss of flame, Taek-Gyu's sharp intake of breath",
                "story_flow": "Jin-hoo playfully yet ruthlessly threatens to incinerate Taek-gyu's prized figurines."
            },
            {
                "timestamp": "3s-4.5s",
                "label": "HOSTAGE CRISIS PANIC",
                "page_number": 7,
                "page_file": "page_007.webp",
                "scene_title": "Hostage Crisis Panic",
                "action": "Taek-Gyu lunges with outstretched hands in theatrical panic, shielding his beloved plastic idol with his own body.",
                "camera": "Fast snap-zoom on Taek-Gyu frantically waving his hands, 28mm lens",
                "vo": '(Oh Taek-Gyu): "(screaming in comic despair, panicked tears) Put the lighter down! Anything but the limited edition! I\'ll give it to you, I swear! Put it down!!" ',
                "sfx": "Clattering desk items, comical frantic scuffling",
                "story_flow": "Taek-gyu erupts in comical panic, treating the figurine threat as a life-or-death hostage situation."
            },
            {
                "timestamp": "4.5s-6s",
                "label": "THE TAX TRAP",
                "page_number": 8,
                "page_file": "page_008.webp",
                "scene_title": "Sister's Tax Warning",
                "action": "Taek-Gyu collapses back into his chair, rubbing his forehead as he reveals the grim reality of South Korea's astronomical capital gains taxes.",
                "camera": "Medium shot tracking Taek-Gyu slouching into his chair, 50mm lens",
                "vo": '(Oh Taek-Gyu): "(exhausted, serious sigh) But listen... my sister warned me. If we cash out thirteen billion into Korean accounts, the government takes over forty percent in taxes!"',
                "sfx": "Heavy keyboard sigh, mouse click",
                "story_flow": "Taek-gyu explains that his sister warned him he could owe billions in taxes on the Bantcoin profits."
            },
            {
                "timestamp": "6s-8s",
                "label": "DELLA ISLAND TAX HAVEN",
                "page_number": 8,
                "page_file": "page_008.webp",
                "scene_title": "Offshore Tax Haven on Della Island",
                "action": "Taek-Gyu turns his monitor around, revealing the incorporation papers of 'OTK Company' registered in an offshore tax haven on Della Island.",
                "camera": "Smooth over-the-shoulder pan across the glowing digital legal registry, 35mm lens",
                "vo": '(Oh Taek-Gyu): "(smug, whispered mastermind pride) That\'s why I already set up a paper company in Della Island: OTK Company. Zero capital gains tax!"',
                "sfx": "Digital folder chime, paper rustle",
                "story_flow": "Taek-gyu details his offshore tax avoidance scheme, revealing he incorporated 'OTK Company' on Della Island."
            },
            {
                "timestamp": "8s-10s",
                "label": "THE PARTNERSHIP PLEDGE",
                "page_number": 9,
                "page_file": "page_009.webp",
                "scene_title": "Taek-gyu's Solemn Pledge",
                "action": "Taek-Gyu places a hand over his heart in a sworn covenant of loyalty between brothers, while Jin-Hoo nods with deep respect. End on a complete freeze frame: subject holds final pose, eyes and hands still, no new action.",
                "camera": "Two-shot of Jin-Hoo and Taek-Gyu exchanging an unspoken vow of trust, locked static hold through 10s",
                "vo": '(Oh Taek-Gyu): "(deep, heartfelt conviction) You have my word as Oh Taek-Gyu. Every single won of your 1.24 billion is yours. We conquer this together."',
                "sfx": "Heartfelt hand-on-chest thump, warm resonant chord; final impact, then silence",
                "story_flow": "Taek-gyu wholeheartedly commits to transferring Jin-hoo's share, showing genuine loyalty beneath his goofy demeanor."
            }
        ]
    },
    {
        "block_title": "The 500 Million Won Wire",
        "duration_sec": 10,
        "format": "9:16 vertical video",
        "source_pages": ["page_009.webp", "page_010.webp", "page_011.webp"],
        "beats": [
            {
                "timestamp": "0s-1.5s",
                "label": "THE FIRST WIRE",
                "page_number": 9,
                "page_file": "page_009.webp",
                "scene_title": "Arrival at KH Bank",
                "action": "Jin-Hoo stands outside KH Bank on a bustling Seoul avenue; his smartphone buzzes violently with an incoming transaction alert.",
                "camera": "Medium shot of Jin-Hoo checking his phone against the glass facade of the bank, 35mm lens",
                "vo": '(Narrator): "(crisp, dynamic financial announcement) Discharge day. Staged transfer protocol initiated: first payment of 500 million won completed."',
                "sfx": "Phone double-vibration buzz, chime of banking notification",
                "story_flow": "Establishes Jin-hoo's presence at KH Bank on his military discharge day."
            },
            {
                "timestamp": "1.5s-3s",
                "label": "PASSBOOK EUPHORIA",
                "page_number": 9,
                "page_file": "page_009.webp",
                "scene_title": "Euphoria Over the Passbook",
                "action": "Close-up of the crisp printed bank passbook: the digital ink clearly reads 500,000,000 KRW deposited into Kang Jin-Hoo's personal account.",
                "camera": "Tight top-down tilt onto the stamped passbook page held in trembling hands, 50mm lens",
                "vo": '(Kang Jin-Hoo): "(exhaling in breathless euphoria, heart racing) Five hundred million won... It\'s really in my account. This isn\'t a dream!"',
                "sfx": "Paper page turn, deep trembling gasp",
                "story_flow": "Jin-hoo is overcome with excitement and relief after confirming his 500 million won initial deposit."
            },
            {
                "timestamp": "3s-4.5s",
                "label": "GIFT TAX STRATEGY",
                "page_number": 10,
                "page_file": "page_010.webp",
                "scene_title": "Flashback: Progressive Gift Tax",
                "action": "Flashback insert to Taek-Gyu explaining why the money must arrive in tranches to navigate Korea's progressive gift tax laws cleanly.",
                "camera": "Quick Dutch angle cut to Taek-Gyu adjusting his glasses over financial docs, 40mm lens",
                "vo": '(Oh Taek-Gyu): "(pragmatic, analytical cadence) Gift tax rules are brutal. I\'ll send five hundred million first. The rest follows once the Della Island routing clears."',
                "sfx": "Swift paper slide, keyboard rattle",
                "story_flow": "Demonstrates financial literacy regarding Korean gift tax regulations and offshore capital distribution."
            },
            {
                "timestamp": "4.5s-6s",
                "label": "FILIAL DEVOTION",
                "page_number": 11,
                "page_file": "page_011.webp",
                "scene_title": "Filial Thoughts on the Street",
                "action": "Jin-Hoo walks along the sunny Seoul boulevard, clutching his bankbook with a warm, tender determination filling his chest.",
                "camera": "Tracking medium profile shot moving with Jin-Hoo's brisk, confident stride, 50mm lens",
                "vo": '(Kang Jin-Hoo): "(tender, resolute, deeply emotional) Mom spent her whole life suffering to pay my tuition. The first thing I\'m doing is making sure she never has to work another day."',
                "sfx": "Distant street music, gentle breeze rustling urban street trees",
                "story_flow": "Establishes Jin-hoo's first priority with his money: treating his mother and helping her quit manual labor."
            },
            {
                "timestamp": "6s-8s",
                "label": "THE LUXURY ATRIUM",
                "page_number": 11,
                "page_file": "page_011.webp",
                "scene_title": "Arrival at the Department Store",
                "action": "Jin-Hoo steps through grand revolving glass doors into the opulent, gleaming marble atrium of a premier high-end luxury department store.",
                "camera": "Wide soaring crane shot sweeping up through multi-story marble balconies and crystal chandeliers, 24mm lens",
                "vo": '(Kang Jin-Hoo): "(awed, ambitious stride) Premier designer boutiques, fine jewelry, imported fashion. Only the finest things for my mother today."',
                "sfx": "Grand atrium acoustic resonance, soft high-society violin background music",
                "story_flow": "Establishes the location of Jin-hoo's shopping trip at a prominent luxury department store."
            },
            {
                "timestamp": "8s-10s",
                "label": "ENTERING THE BOUTIQUE",
                "page_number": 11,
                "page_file": "page_011.webp",
                "scene_title": "Jin-hoo Begins Browsing",
                "action": "Jin-Hoo smiles brightly as he approaches an elegant designer fashion boutique, reaching for the golden door handle as the scene freezes into anticipation. End on a complete freeze frame: subject holds final pose, eyes and hands still, no new action.",
                "camera": "Medium tracking shot pushing toward Jin-Hoo's hopeful, smiling face, locked static hold through 10s",
                "vo": '(Kang Jin-Hoo): "(warm, loving happiness) Wait for me, Mom. Your son is going to give you the world."',
                "sfx": "Elegant glass door glide, soft piano flourish; final impact, then silence",
                "story_flow": "Jin-hoo looks around the high-end retail floor in good spirits, planning to buy gifts for his mother."
            }
        ]
    },
    {
        "block_title": "The Humiliation at the Department Store",
        "duration_sec": 10,
        "format": "9:16 vertical video",
        "source_pages": ["page_011.webp", "page_012.webp", "page_013.webp"],
        "beats": [
            {
                "timestamp": "0s-1.5s",
                "label": "THE HARSH COMMOTION",
                "page_number": 11,
                "page_file": "page_011.webp",
                "scene_title": "Sudden Outburst in the Hallway",
                "action": "A screeching, shrill voice shatters the refined department store atmosphere; upscale shoppers turn their heads in discomfort.",
                "camera": "Fast whip-pan across startled wealthy shoppers in designer clothing, 35mm lens",
                "vo": '(Wealthy VIP Customer): "(shrill, arrogant screeching fury) What the hell are you doing, you filthy old hag?! Keep your dirty hands off my shoes!"',
                "sfx": "Sharp gasp from nearby shoppers, harsh clattering of a dropped cleaning bucket",
                "story_flow": "A furious customer publicly screams at a female cleaning worker over a dirty cleaning rag."
            },
            {
                "timestamp": "1.5s-3s",
                "label": "THE MURMURING CROWD",
                "page_number": 11,
                "page_file": "page_011.webp",
                "scene_title": "Whispers of Disapproval Among Bystanders",
                "action": "Bystanders and wealthy mall patrons gather in a tight circle, whispering uncomfortably as the aggressive woman continues her public tirade.",
                "camera": "Medium crowd reaction shot showing onlookers whispering behind hands, 40mm lens",
                "vo": '(Bystander): "(whispered, shocked discomfort) How awful... Does she really have to humiliate an elderly cleaner like that in public?"',
                "sfx": "Murmuring crowd whispers, tense footsteps shuffling",
                "story_flow": "Surrounding department store shoppers mutter among themselves, disgusted by the scene."
            },
            {
                "timestamp": "3s-4.5s",
                "label": "THE VERBAL ABUSE",
                "page_number": 12,
                "page_file": "page_012.webp",
                "scene_title": "Verbal Abuse Over Shoes",
                "action": "A haughty middle-aged woman adorned in ostentatious designer jewelry points a manicured finger downward at a cleaning worker with venomous disdain.",
                "camera": "Low-angle dramatic tilt up toward the sneering, furious VIP customer, 50mm lens",
                "vo": '(Wealthy VIP Customer): "(venomous, haughty cruelty) Do you have any idea how much these imported shoes cost?! You couldn\'t afford one lace with a year of your pitiful wages!"',
                "sfx": "Harsh heel tap on marble, venomous sneer breath",
                "story_flow": "Escalates the abusive customer's entitlement and cruelty, viciously demeaning the worker's manual labor."
            },
            {
                "timestamp": "4.5s-6s",
                "label": "THE FORCED KNEELING",
                "page_number": 12,
                "page_file": "page_012.webp",
                "scene_title": "Forced Humiliation",
                "action": "The suit-clad store manager bows subserviently, then aggressively orders the trembling cleaning worker on the wet floor to get on her knees and beg.",
                "camera": "High-angle sharp cut looking down at the small, trembling cleaning worker on the wet tiles, 50mm lens",
                "vo": '(Store Manager): "(cold, cowardly hiss) What are you just sitting there for, Auntie?! Get on your knees and apologize to the customer right now!!" ',
                "sfx": "Harsh knee impact on cold marble tile, quiet weeping sob",
                "story_flow": "The manager forces the older cleaning woman to bow and beg for forgiveness on the floor."
            },
            {
                "timestamp": "6s-8s",
                "label": "JIN-HOO PUSHES THROUGH",
                "page_number": 12,
                "page_file": "page_012.webp",
                "scene_title": "Horrifying Truth",
                "action": "Hearing the commotion, Jin-Hoo's expression darkens. He elbows through the circle of onlookers, his eyes widening in mounting dread as he recognizes the frail, trembling figure on the floor.",
                "camera": "Intense dolly-zoom pushing in on Jin-Hoo's face as the crowd blurs around him, 85mm portrait lens",
                "vo": '(Kang Jin-Hoo): "(gasping in mounting horror, voice breaking) No... That gray hair... That faded blue work uniform... That can\'t be..."',
                "sfx": "Muffled heartbeat thumping like a war drum, crowd voices fading into a deafening ring",
                "story_flow": "Jin-hoo recognizes the woman being abused, panic overtaking his composure."
            },
            {
                "timestamp": "8s-10s",
                "label": "THE DEVASTATING TRUTH",
                "page_number": 13,
                "page_file": "page_013.webp",
                "scene_title": "Devastating Realization",
                "action": "Jin-Hoo breaks through the front row: kneeling on the cold marble floor with tear-stained cheeks and trembling hands is his own beloved mother. Jin-Hoo freezes in agonizing shock and boundless fury. End on a complete freeze frame: subject holds final pose, eyes and hands still, no new action.",
                "camera": "Dramatic low-angle close-up framing Jin-Hoo's devastated, trembling face looking down, cutting to his mother's tearful face, locked static hold through 10s",
                "vo": '(Kang Jin-Hoo): "(raw, agonizing, heartbroken cry) MOM...?! That\'s my mother...!!" ',
                "sfx": "Heavy shattering glass chord, dramatic low orchestral rumble; final impact, then silence",
                "story_flow": "Confirms Jin-hoo's devastating realization that the cleaning woman being publicly humiliated and ordered to kneel is his own mother."
            }
        ]
    }
]

story = {
    "title": "The Investor Who Sees The Future",
    "chapter": "2",
    "format": "SERYE drama block storyboard",
    "block_duration_sec": 10,
    "blocks": BLOCKS
}

# Write storyboard_9_16.json
(OUT_DIR / "storyboard_9_16.json").write_text(json.dumps(story, indent=2, ensure_ascii=False), encoding="utf-8")
print("[OK] storyboard_9_16.json written")

# Render Markdown
lines = [
    f"# SERYE Drama Storyboard — {story['title']} — Chapter {story['chapter']}",
    "",
    "Format: 9:16 vertical · 10 seconds per block · six timestamped beats per block",
    ""
]
for n, block in enumerate(story["blocks"], 1):
    lines += [
        f"## SERYE DRAMA BLOCK {n} — {block['block_title']}",
        "",
        "| Time | Panel label | Source | Action / composition | Camera | VO / dialogue | SFX |",
        "|---|---|---|---|---|---|---|"
    ]
    for beat in block["beats"]:
        def cell(value): return str(value).replace("|", "\\|").replace("\n", " ")
        lines.append("| " + " | ".join(cell(beat[k]) for k in ["timestamp", "label", "page_file", "action", "camera", "vo", "sfx"]) + " |")
    lines += ["", "FINAL BEAT: freeze frame / held pose through 10s. No extra movement.", "", "---", ""]

(OUT_DIR / "storyboard_9_16.md").write_text("\n".join(lines), encoding="utf-8")
print("[OK] storyboard_9_16.md written")

# Render HTML
css = """
    :root{--bg:#08090d;--panel:#131722;--line:#32394a;--text:#f2f4f8;--muted:#aeb8ca;--gold:#f2c14e;--cyan:#62d9ff}
    *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.4 system-ui,sans-serif}main{max-width:1500px;margin:auto;padding:24px}h1{margin:0 0 6px;font-size:clamp(22px,4vw,38px)}h2{margin:0;color:#fff;font-size:22px}.sub{color:var(--muted);margin-bottom:24px}.block{border:1px solid var(--line);border-radius:14px;background:var(--panel);padding:16px;margin:0 0 28px}.blockhead{display:flex;justify-content:space-between;gap:10px;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:14px}.tag{color:var(--gold);font-weight:800;letter-spacing:.08em;text-transform:uppercase}.strip{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.beat{min-width:0;border:1px solid var(--line);background:#0d111a;border-radius:9px;overflow:hidden}.thumb{aspect-ratio:9/11;background:#222;position:relative;overflow:hidden}.thumb img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:.65}.time{position:absolute;left:7px;top:7px;background:#000d;color:var(--gold);font-weight:800;padding:3px 6px;border-radius:4px}.label{position:absolute;left:7px;right:7px;bottom:7px;background:#000d;color:#fff;font-weight:900;padding:4px 6px;border-radius:4px;letter-spacing:.04em}.content{padding:9px}.content h3{margin:0 0 5px;color:var(--cyan);font-size:14px}.content p{margin:5px 0;color:var(--muted);font-size:12px}.content b{color:#fff}.freeze{border:1px solid var(--gold);color:var(--gold);padding:7px;margin-top:12px;border-radius:6px;font-weight:700}.topnote{padding:12px;border:1px solid var(--line);border-radius:10px;color:var(--muted);margin:16px 0}
"""
out_html = [
    "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>SERYE Storyboard — Chapter 2</title><style>",
    css,
    "</style></head><body><main>",
    f"<h1>SERYE DRAMA STORYBOARD — {html.escape(story['title'])} — CHAPTER {html.escape(str(story['chapter']))}</h1>",
    "<div class='sub'>9:16 vertical · 10 seconds per block · six-panel director strips · canonical sequential image analysis</div>",
    "<div class='topnote'><b>Storyboard contract:</b> Each block runs 10 seconds. Each strip shows six timestamped beats. Last beat freezes on final pose. This is a planning artifact, not a Flow image ingredient.</div>"
]
for n, block in enumerate(story["blocks"], 1):
    out_html.append(f"<section class='block'><div class='blockhead'><div><div class='tag'>SERYE DRAMA BLOCK {n}</div><h2>{html.escape(block['block_title'])}</h2></div><div class='tag'>10s · 9:16</div></div><div class='strip'>")
    for beat in block["beats"]:
        src = "images/" + html.escape(beat["page_file"])
        out_html.append("<article class='beat'>")
        out_html.append(f"<div class='thumb'><img src='{src}' alt='{html.escape(beat['page_file'])}'><div class='time'>{html.escape(beat['timestamp'])}</div><div class='label'>{html.escape(beat['label'])}</div></div>")
        out_html.append("<div class='content'>")
        out_html.append(f"<h3>{html.escape(beat['scene_title'])}</h3>")
        out_html.append(f"<p><b>Action:</b> {html.escape(beat['action'])}</p>")
        out_html.append(f"<p><b>Camera:</b> {html.escape(beat['camera'])}</p>")
        out_html.append(f"<p><b>VO:</b> {html.escape(beat['vo'])}</p>")
        out_html.append(f"<p><b>SFX:</b> {html.escape(beat['sfx'])}</p>")
        out_html.append(f"<p><b>Source:</b> {html.escape(beat['page_file'])} (page {beat['page_number']})</p>")
        out_html.append("</div></article>")
    out_html.append("</div><div class='freeze'>FINAL BEAT: freeze frame held pose through 10s. Subject locks final pose, eyes and hands still, zero extra movement.</div></section>")

out_html.append("</main></body></html>")
(OUT_DIR / "storyboard_9_16.html").write_text("\n".join(out_html), encoding="utf-8")
print("[OK] storyboard_9_16.html written")
