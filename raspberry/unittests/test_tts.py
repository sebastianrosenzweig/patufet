import unittest

import soundfile as sf
from patufet.tts import synthesize


class TestTTS(unittest.TestCase):
    def test_transcribe_audio_with_test_file(self):
        audio, sample_rate = synthesize(
            "Bon dia! Avui fa un dia magnífic a Catalunya."
        )

        sf.write("output.wav", audio, sample_rate)


if __name__ == "__main__":
    unittest.main()
