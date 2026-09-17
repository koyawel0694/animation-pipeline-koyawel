#!/usr/bin/env python3
"""Shared, deterministic helpers for the manga chapter production contract.

The canonical analysis is model-generated, but everything after that boundary
must be deterministic.  Keeping scene identity, text classification, and
script formatting here prevents the storyboard exporter, prompt exporter, and
verifier from silently disagreeing about what the scanned chapter says.
"""

from __future__ import annotations

import re
from typing import Iterable


TEXT_TYPES = {"spoken", "narration", "thought", "sfx", "caption", "unknown"}
_MISSING = {"", "none", "null", "n/a", "na", "unknown", "(none)", "(null)", "[none]"}
_UNREADABLE = {"[unreadable]", "[illegible]", "[unreadable text]"}


def clean_text(value: object) -> str:
    """Collapse whitespace for prompt-safe text while retaining the words."""
    return " ".join(str(value or "").split())


def source_text(value: object) -> str:
    """Trim only the outside of source text; preserve internal line breaks."""
    return str(value or "").strip()


def is_placeholder_text(value: object) -> bool:
    """Identify omitted/unreadable analysis values that must not become audio."""
    normalized = clean_text(value).lower()
    return normalized in _MISSING or normalized in _UNREADABLE


def is_unreadable_text(value: object) -> bool:
    """Identify unreadable analysis placeholders."""
    return clean_text(value).lower() in _UNREADABLE


def normalize_emotion(value: object) -> str:
    """Return a parenthesized delivery cue, or an empty string for sentinels."""
    emotion = clean_text(value)
    if emotion.lower() in _MISSING:
        return ""
    if emotion.startswith("(") and emotion.endswith(")"):
        return emotion
    return f"({emotion})"


def _explicit_text_type(scene: dict) -> str:
    for key in ("text_type", "dialogue_type", "content_type", "transcript_type"):
        value = clean_text(scene.get(key)).lower().replace("-", "_")
        if value in TEXT_TYPES:
            return value
        if value in {"voiceover", "voice_over", "voice"}:
            return "narration"
        if value in {"sound_effect", "sound_effects", "onomatopoeia"}:
            return "sfx"
    if scene.get("is_sfx") is True:
        return "sfx"
    return ""


def scene_text_type(scene: dict) -> str:
    """Classify extracted text without changing the canonical transcript.

    New analyses can provide ``text_type`` explicitly.  The conservative
    fallback handles older analyses, especially short CJK onomatopoeia such as
    ``轰!!`` and ``唰`` that should be sound design rather than spoken VO.
    """
    text = source_text(scene.get("dialogue_text"))
    if not text or is_placeholder_text(text):
        return "none"

    explicit = _explicit_text_type(scene)
    if explicit:
        return explicit

    compact = re.sub(r"\s+", "", text)
    if (
        len(compact) <= 8
        and re.search(r"[\u3400-\u9fff]", compact)
        and not re.search(r"[A-Za-z]{3,}", compact)
    ):
        return "sfx"

    speaker = clean_text(scene.get("speaker")).lower()
    if "thought" in speaker or "inner" in speaker:
        return "thought"
    if "narrat" in speaker or "caption" in speaker:
        return "narration"
    return "spoken"


def ensure_scene_identity(scenes: Iterable[dict]) -> list[dict]:
    """Return scenes with stable page/scene IDs, preserving chronological order."""
    result = []
    per_page: dict[int, int] = {}
    for global_index, original in enumerate(scenes, 1):
        scene = dict(original)
        page_number = int(scene.get("page_number") or 0)
        per_page[page_number] = per_page.get(page_number, 0) + 1
        page_scene_index = int(scene.get("_page_scene_index") or per_page[page_number])
        scene["page_number"] = page_number
        scene["_scene_index"] = global_index
        scene["_page_scene_index"] = page_scene_index
        scene["_scene_key"] = scene.get("_scene_key") or f"p{page_number:03d}-s{page_scene_index:02d}"
        result.append(scene)
    return result


def flatten_scenes(data: dict) -> list[dict]:
    """Flatten page scenes into one ordered list with stable source IDs."""
    scenes = []
    for page in data.get("pages", []):
        page_number = int(page.get("page_number") or 0)
        page_file = page.get("page_file") or ""
        for page_scene_index, raw_scene in enumerate(page.get("scenes") or [], 1):
            scene = dict(raw_scene)
            scene["page_number"] = page_number
            scene["page_file"] = page_file
            scene["_page_scene_index"] = page_scene_index
            scenes.append(scene)
    return ensure_scene_identity(scenes)


def build_script_entries(scenes: Iterable[dict]) -> list[dict]:
    """Build the ordered, source-traceable script ledger from canonical scenes."""
    entries = []
    for scene in ensure_scene_identity(scenes):
        raw = source_text(scene.get("dialogue_text"))
        if not raw or is_placeholder_text(raw):
            continue
        text_type = scene_text_type(scene)
        emotion = normalize_emotion(scene.get("voice_emotion"))
        speaker = clean_text(scene.get("speaker"))
        if not speaker:
            speaker = "Narrator" if text_type in {"narration", "sfx"} else "Unidentified speaker"
        prompt_text = clean_text(raw)
        if text_type != "sfx" and emotion:
            prompt_text = f"{emotion} {prompt_text}"
        entries.append({
            "line_id": scene["_scene_key"],
            "scene_index": scene["_scene_index"],
            "page_number": scene["page_number"],
            "page_file": scene.get("page_file", ""),
            "scene_title": clean_text(scene.get("scene_title")),
            "text_type": text_type,
            "speaker": speaker,
            "voice_emotion": emotion,
            "dialogue_text": raw,
            "prompt_text": prompt_text,
        })
    return entries


def script_cue(beat: dict) -> str:
    """Render the exact beat transcript as an explicit prompt instruction."""
    raw = source_text(beat.get("source_text") or beat.get("dialogue_text"))
    text_type = clean_text(beat.get("text_type")).lower() or ("spoken" if raw else "none")
    if not raw or is_placeholder_text(raw) or text_type == "none":
        return "MANGA SCRIPT: No spoken dialogue or voiceover for this beat. Do not invent dialogue."
    if text_type == "sfx":
        return f"MANGA SOUND EFFECT (not spoken): {clean_text(raw)}"
    speaker = clean_text(beat.get("speaker")) or "Unidentified speaker"
    emotion = normalize_emotion(beat.get("voice_emotion"))
    delivery = f" Delivery: {emotion}." if emotion else ""
    return f'MANGA SCRIPT — Speaker: {speaker}.{delivery} Exact line: "{clean_text(raw)}"'
