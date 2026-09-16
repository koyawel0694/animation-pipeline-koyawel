import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parents[1]))

from build_block_prompts_txt import load_style_profile, style_lines


class StylePresetTests(unittest.TestCase):
    def test_all_presets_have_required_prompt_sections(self):
        config = json.loads((Path(__file__).parents[1] / "style_presets.json").read_text())
        self.assertEqual(
            set(config["presets"]),
            {"photorealistic_live_action", "webtoon_2d", "anime_sakuga_2d", "motion_comic_2d"},
        )
        for profile in config["presets"].values():
            self.assertTrue(all(style_lines(profile)))

    def test_chapter_selection_overrides_global_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            chapter = Path(tmp)
            (chapter / "style_selection.json").write_text(
                json.dumps({"default_preset": "photorealistic_live_action"})
            )
            selected, profile = load_style_profile(chapter)
            self.assertEqual(selected, "photorealistic_live_action")
            self.assertIn("photorealistic live-action", profile["style_anchor"])

    def test_explicit_override_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            selected, profile = load_style_profile(Path(tmp), "motion_comic_2d")
            self.assertEqual(selected, "motion_comic_2d")
            self.assertIn("motion-comic", profile["style_anchor"])


if __name__ == "__main__":
    unittest.main()
