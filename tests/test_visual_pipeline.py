import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parents[1]))

REPO_ROOT = Path(__file__).parents[1]

from generate_nano_storyboards import build_block_specs
from manga_pipeline import storyboard_asset_command, visual_generation_command


class VisualPipelineTests(unittest.TestCase):
    def test_block_specs_follow_chapter_storyboard_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            chapter = Path(tmp)
            (chapter / "storyboard_9_16.json").write_text(json.dumps({
                "title": "Demo",
                "chapter": "2",
                "blocks": [{
                    "block_title": "The New Question",
                    "beats": [
                        {"label": "OPENING", "page_file": "page_003.webp"},
                        {"label": "REVEAL", "page_file": "page_004.webp"},
                    ],
                }],
            }), encoding="utf-8")

            specs = build_block_specs(chapter)

            self.assertEqual(specs[0][0], "block01_the_new_question")
            self.assertEqual(specs[0][1], "Block 1 — The New Question")
            self.assertEqual(specs[0][2], ["page_003.webp", "page_004.webp"])
            self.assertEqual(specs[0][3], ["OPENING", "REVEAL"])

    def test_visual_stage_passes_chapter_directory_and_shared_character_refs(self):
        command = visual_generation_command(
            Path("/tmp/ch2"),
            "/usr/bin/python3",
            Path("/tmp/ch1/character_refs"),
        )
        self.assertEqual(command[:3], ["/usr/bin/python3", str(REPO_ROOT / "generate_nano_storyboards.py"), "--chapter-dir"])
        self.assertEqual(command[3:], ["/tmp/ch2", "--reference-dir", "/tmp/ch1/character_refs", "--all"])

    def test_existing_chapter_one_refs_are_resolved_for_chapter_two(self):
        from manga_pipeline import resolve_character_reference_dir

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            refs = root / "ch1" / "character_refs"
            refs.mkdir(parents=True)
            self.assertEqual(resolve_character_reference_dir(root / "ch2"), refs)

    def test_storyboard_asset_command_uses_known_refs_and_local_compositor(self):
        command = storyboard_asset_command(Path("/tmp/ch2"), "/usr/bin/python3", Path("/tmp/ch1/character_refs"))
        self.assertEqual(command, [
            "/usr/bin/python3",
            str(REPO_ROOT / "compose_chapter_storyboards.py"),
            "--chapter-dir", "/tmp/ch2",
            "--reference-dir", "/tmp/ch1/character_refs",
        ])


if __name__ == "__main__":
    unittest.main()
