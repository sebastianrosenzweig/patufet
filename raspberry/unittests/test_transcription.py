import unittest
from transcription import transcribe_audio

class TestTranscription(unittest.TestCase):
    def test_transcribe_audio_with_test_file(self):
        # This test runs the actual model on test.wav
        result = transcribe_audio("unittests/test.wav")
        self.assertIn("digue'm com estàs", result.lower())

if __name__ == "__main__":
    unittest.main()
