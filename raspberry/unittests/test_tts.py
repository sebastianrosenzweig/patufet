import unittest

import soundfile as sf
from patufet.tts import synthesize


class TestTTS(unittest.TestCase):
    def test_synthesize_audio_with_test_string(self):
        audio, sample_rate = synthesize(
            "Bon dia! Avui fa un dia magnífic a Catalunya."
        )

        assert sample_rate == 22050
        assert len(audio) >= 22050
