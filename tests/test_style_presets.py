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
        expected = {
            "photorealistic_live_action",
            "studio_ghibli",
            "webtoon_2d",
            "anime_sakuga_2d",
            "stylized_3d_animation",
            "dark_fantasy_anime",
            "motion_comic_2d",
            "cyberpunk_neon",
            "classic_comic_book",
        }
        self.assertTrue(expected.issubset(set(config["presets"])))
        for name, profile in config["presets"].items():
            self.assertTrue(all(style_lines(profile)), f"Missing style lines in {name}")
            self.assertIn("character_ref_style", profile, f"Missing character_ref_style in {name}")
            self.assertIn("storyboard_style", profile, f"Missing storyboard_style in {name}")

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
