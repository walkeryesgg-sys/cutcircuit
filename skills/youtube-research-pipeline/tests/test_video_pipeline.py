import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "video_pipeline.py"
SPEC = importlib.util.spec_from_file_location("video_pipeline", SCRIPT)
PIPELINE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PIPELINE)


class VideoPipelineTests(unittest.TestCase):
    def test_audio_envelope_survives_small_quantization_changes(self):
        self.assertGreaterEqual(
            PIPELINE.audio_envelope_similarity("777788889999aaaa", "77778889999aaaab"),
            0.9,
        )

    def test_official_source_does_not_replace_target_participation(self):
        registry = {"sources": [{"name": "Lex Fridman", "titleTerms": ["lex fridman"], "provenanceScore": 32}]}
        score, reasons = PIPELINE.quality_score({
            "title": "Sam Altman: OpenAI, Elon Musk and AGI | Lex Fridman Podcast",
            "channelTitle": "Lex Fridman",
            "durationSeconds": 7200,
        }, registry)
        self.assertIn("target_speaker_not_primary", reasons)
        self.assertLess(score, 60)

    def test_original_interviewer_receives_provenance_credit(self):
        registry = {"sources": [{"name": "Everyday Astronaut", "channelId": "UC-ORIGINAL", "provenanceScore": 32}]}
        points, source = PIPELINE.provenance_score({
            "channelId": "UC-ORIGINAL",
            "channelTitle": "Renamed Channel",
            "title": "First Look Inside Starfactory with Elon Musk",
        }, registry)
        self.assertEqual(points, 32)
        self.assertEqual(source, "Everyday Astronaut")


if __name__ == "__main__":
    unittest.main()
