import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from build_serye_storyboard import build_storyboard


class EpisodicPacingTests(unittest.TestCase):
    def _create_mock_chapter(self, num_pages: int, scenes_per_page: int = 3):
        pages = []
        scenes = []
        for p in range(1, num_pages + 1):
            page_scenes = []
            for s in range(1, scenes_per_page + 1):
                scene_dict = {
                    "scene_title": f"Page {p} Scene {s}",
                    "action_description": f"Character performs action on page {p}",
                    "camera_movement": "Push in slowly",
                    "dialogue_text": f"Line of dialogue {p}-{s}",
                    "voice_emotion": "intense",
                    "visual_style_fx": "subtle lighting",
                    "story_flow": f"Story beat {p}-{s}",
                    "page_number": p,
                    "page_file": f"page_{p:03d}.webp",
                    "_scene_id": len(scenes) + len(page_scenes),
                }
                page_scenes.append(scene_dict)
                scenes.append(scene_dict)
            pages.append({"page_number": p, "page_file": f"page_{p:03d}.webp", "scenes": page_scenes})

        data = {
            "title": "Test Manga Series",
            "chapter": "1",
            "pages": pages,
        }
        return data, scenes

    def test_short_chapter_defaults_to_single_60s_episode(self):
        data, scenes = self._create_mock_chapter(num_pages=18)
        story, episodes = build_storyboard(data, scenes)

        self.assertEqual(story["total_episodes"], 1)
        self.assertEqual(story["total_blocks"], 6)
        self.assertEqual(story["total_duration_sec"], 60)
        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["page_range"], [1, 18])
        self.assertTrue(episodes[0]["blocks"][-1]["beats"][-1]["is_cliffhanger"])

    def test_long_chapter_segments_into_multi_part_episodes(self):
        # 63-page chapter (like Infinite Mage Ch 1)
        data, scenes = self._create_mock_chapter(num_pages=63)
        story, episodes = build_storyboard(data, scenes, pages_per_episode=22)

        self.assertEqual(story["total_episodes"], 3)
        self.assertEqual(story["total_blocks"], 18)
        self.assertEqual(story["total_duration_sec"], 180)
        self.assertEqual(len(episodes), 3)

        # Check episode 1
        self.assertEqual(episodes[0]["episode_number"], 1)
        self.assertEqual(episodes[0]["page_range"], [1, 21])
        self.assertEqual(episodes[0]["duration_sec"], 60)
        self.assertEqual(len(episodes[0]["blocks"]), 6)
        self.assertTrue(episodes[0]["blocks"][-1]["beats"][-1]["is_cliffhanger"])

        # Check episode 2
        self.assertEqual(episodes[1]["episode_number"], 2)
        self.assertEqual(episodes[1]["page_range"], [22, 42])
        self.assertEqual(episodes[1]["duration_sec"], 60)
        self.assertEqual(len(episodes[1]["blocks"]), 6)
        self.assertTrue(episodes[1]["blocks"][-1]["beats"][-1]["is_cliffhanger"])

        # Check episode 3
        self.assertEqual(episodes[2]["episode_number"], 3)
        self.assertEqual(episodes[2]["page_range"], [43, 63])
        self.assertEqual(episodes[2]["duration_sec"], 60)
        self.assertEqual(len(episodes[2]["blocks"]), 6)
        self.assertTrue(episodes[2]["blocks"][-1]["beats"][-1]["is_cliffhanger"])


if __name__ == "__main__":
    unittest.main()
