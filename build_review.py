#!/usr/bin/env python3
"""
build_review.py — Build a manga review video from images + narration.

Pipeline:
  1. TTS narration → audio.mp3 + word timestamps
  2. Ken-Burns slideshow of manga images synced to narration segments
  3. Groq word-synced captions burned in
  4. Final output: review.mp4

Usage:
    python3 build_review.py <images_dir> <narration.txt> [--output review.mp4]
"""

import os
import sys
import json
import subprocess
import argparse
import tempfile
import asyncio
import re
from pathlib import Path
from math import ceil


# ---------------------------------------------------------------------------
# STAGE 1: TTS via edge-tts
# ---------------------------------------------------------------------------

def tts_generate(narration: str, audio_out: str, voice: str = "en-US-GuyNeural") -> dict:
    """Generate TTS audio + word-level timestamps using edge-tts."""
    print(f"[TTS] Generating audio with voice '{voice}'...")
    cmd = [
        sys.executable, "-m", "edge_tts",
        "--text", narration,
        "--voice", voice,
        "--write-media", audio_out,
        "--write-subtitles", audio_out.replace(".mp3", ".vtt"),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"[TTS] Audio: {audio_out}")
    return {"audio": audio_out, "vtt": audio_out.replace(".mp3", ".vtt")}


def get_audio_duration(audio_path: str) -> float:
    """Get duration of audio file in seconds."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", audio_path],
        capture_output=True, text=True
    )
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


# ---------------------------------------------------------------------------
# STAGE 2: Parse VTT subtitles into timed segments
# ---------------------------------------------------------------------------

def parse_vtt(vtt_path: str) -> list:
    """Parse VTT subtitle file into list of {start, end, text} dicts."""
    segments = []
    with open(vtt_path) as f:
        content = f.read()

    # Split on blank lines
    blocks = re.split(r'\n\n+', content.strip())
    for block in blocks:
        lines = block.strip().split('\n')
        for i, line in enumerate(lines):
            if '-->' in line:
                times = line.split('-->')
                start = vtt_time_to_seconds(times[0].strip())
                end = vtt_time_to_seconds(times[1].strip())
                text = ' '.join(lines[i+1:]).strip()
                if text:
                    segments.append({"start": start, "end": end, "text": text})
                break
    return segments


def vtt_time_to_seconds(t: str) -> float:
    """Convert VTT timestamp to seconds."""
    parts = t.replace(',', '.').split(':')
    if len(parts) == 3:
        return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
    elif len(parts) == 2:
        return float(parts[0])*60 + float(parts[1])
    return float(parts[0])


# ---------------------------------------------------------------------------
# STAGE 3: Ken-Burns image segments
# ---------------------------------------------------------------------------

def create_kenburns_segment(image_path: str, duration: float, output_path: str,
                            direction: str = "zoom_in", resolution: str = "1920x1080") -> str:
    """Create a Ken-Burns (zoom/pan) effect segment from a single image."""
    w, h = resolution.split("x")

    # Alternate zoom in / zoom out / pan left / pan right for variety
    effects = {
        "zoom_in":  f"scale=8000:-1,zoompan=z='min(zoom+0.001,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(duration*25)}:s={resolution}:fps=25",
        "zoom_out": f"scale=8000:-1,zoompan=z='if(eq(on,1),1.5,max(zoom-0.001,1.0))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(duration*25)}:s={resolution}:fps=25",
        "pan_left": f"scale=8000:-1,zoompan=z='1.3':x='iw/2-(iw/zoom/2)+((iw/zoom)*0.3)*(1-on/{int(duration*25)})':y='ih/2-(ih/zoom/2)':d={int(duration*25)}:s={resolution}:fps=25",
        "pan_right":f"scale=8000:-1,zoompan=z='1.3':x='iw/2-(iw/zoom/2)-((iw/zoom)*0.3)*(1-on/{int(duration*25)})':y='ih/2-(ih/zoom/2)':d={int(duration*25)}:s={resolution}:fps=25",
    }
    effect = effects.get(direction, effects["zoom_in"])

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-vf", f"scale=8000:-1:flags=lanczos,{effect}",
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def create_blur_transition(prev_image: str, next_image: str, duration: float,
                           output_path: str, resolution: str = "1920x1080") -> str:
    """Create a smooth crossfade transition between two images.
    Uses a short fade-in on the next image for a cinematic look."""
    w, h = resolution.split("x")
    frames = max(int(duration * 25), 3)  # minimum 3 frames

    # Simple approach: fade-in the next image over the transition duration
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", next_image,
        "-vf", (
            f"scale=8000:-1:flags=lanczos,"
            f"zoompan=z='1.3':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={frames}:s={resolution}:fps=25,"
            f"fade=t=in:st=0:d={duration}"
        ),
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


# ---------------------------------------------------------------------------
# STAGE 4: Assemble slideshow synced to narration segments
# ---------------------------------------------------------------------------

def build_slideshow(images: list, vtt_segments: list, output_dir: str, resolution: str = "1920x1080") -> str:
    """Build Ken-Burns slideshow synced to VTT narration segments."""

    slides_dir = Path(output_dir) / "slides"
    slides_dir.mkdir(exist_ok=True)

    directions = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
    segments = []

    # Group VTT segments into chunks that map to images
    # Each image gets roughly equal screen time
    total_duration = vtt_segments[-1]["end"] if vtt_segments else 60
    num_images = len(images)
    time_per_image = total_duration / max(num_images, 1)

    concat_file = slides_dir / "concat.txt"
    concat_entries = []

    for i, img in enumerate(images):
        start_time = i * time_per_image
        end_time = min((i + 1) * time_per_image, total_duration)
        duration = end_time - start_time

        direction = directions[i % len(directions)]
        slide_out = str(slides_dir / f"slide_{i:03d}.mp4")

        print(f"  [SLIDE {i+1}/{num_images}] {Path(img).name} → {duration:.1f}s ({direction})")
        create_kenburns_segment(img, duration, slide_out, direction, resolution)
        concat_entries.append(f"file '{Path(slide_out).resolve()}'")

        # Add blur transition between slides (not after the last one)
        if i < num_images - 1:
            trans_dur = 0.3  # 300ms blur transition
            trans_out = str(slides_dir / f"trans_{i:03d}.mp4")
            next_img = images[i + 1]
            print(f"  [TRANS {i+1}/{num_images-1}] blur transition {trans_dur:.1f}s")
            create_blur_transition(img, next_img, trans_dur, trans_out, resolution)
            concat_entries.append(f"file '{Path(trans_out).resolve()}'")

    # Concat all slides
    concat_file.write_text("\n".join(concat_entries))
    slideshow_out = str(slides_dir / "slideshow.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p",
        slideshow_out
    ], check=True, capture_output=True)

    print(f"[SLIDESHOW] {num_images} slides → {slideshow_out}")
    return slideshow_out


# ---------------------------------------------------------------------------
# STAGE 5: Merge audio + video + captions
# ---------------------------------------------------------------------------

def merge_with_captions(video_path: str, audio_path: str, vtt_path: str,
                        output_path: str) -> str:
    """Merge slideshow video with TTS audio (no burned-in subtitles)."""
    print("[MERGE] Combining video + audio...")

    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        output_path
    ], check=True, capture_output=True)

    print(f"[DONE] Review video: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Build manga review video")
    parser.add_argument("images_dir", help="Directory containing page images")
    parser.add_argument("narration", help="Path to narration.txt")
    parser.add_argument("--output", "-o", default="review.mp4", help="Output video file")
    parser.add_argument("--voice", default="en-US-GuyNeural", help="TTS voice name")
    parser.add_argument("--resolution", default="1920x1080", help="Video resolution")
    parser.add_argument("--skip-tts", action="store_true", help="Skip TTS, use existing audio.mp3 + narration.vtt")
    args = parser.parse_args()

    images_dir = Path(args.images_dir)
    narration_path = Path(args.narration)
    work_dir = Path(args.output).parent
    work_dir.mkdir(parents=True, exist_ok=True)

    # Collect images
    images = sorted([
        str(p) for p in images_dir.iterdir()
        if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp')
    ])
    if not images:
        print(f"[ERROR] No images found in {images_dir}")
        sys.exit(1)
    print(f"[INPUT] {len(images)} images from {images_dir}")

    narration = narration_path.read_text().strip()
    print(f"[INPUT] Narration: {len(narration)} chars ({len(narration.split())} words)")

    # TTS
    audio_path = str(work_dir / "audio.mp3")
    vtt_path = audio_path.replace(".mp3", ".vtt")

    if args.skip_tts and Path(audio_path).exists() and Path(vtt_path).exists():
        print("[TTS] Skipping — using existing audio.mp3 + narration.vtt")
    else:
        tts_generate(narration, audio_path, voice=args.voice)

    # VTT segments
    vtt_segments = parse_vtt(vtt_path)
    if not vtt_segments:
        print("[ERROR] No VTT segments found. Check TTS output.")
        sys.exit(1)
    total_dur = vtt_segments[-1]["end"]
    print(f"[TIMING] {len(vtt_segments)} subtitle cues, total {total_dur:.1f}s")

    # Build slideshow
    slideshow = build_slideshow(images, vtt_segments, str(work_dir), args.resolution)

    # Merge everything
    final = merge_with_captions(slideshow, audio_path, vtt_path, args.output)
    print(f"\n[SUCCESS] Manga review video ready: {final}")
    dur = get_audio_duration(final)
    print(f"  Duration: {dur:.1f}s | Resolution: {args.resolution}")


if __name__ == "__main__":
    main()
