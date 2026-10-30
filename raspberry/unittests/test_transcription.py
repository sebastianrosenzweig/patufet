import unittest

import numpy as np
from patufet.transcription import transcribe_audio

class TestTranscription(unittest.TestCase):
    def test_transcribe_empty_audio(self):
        result = transcribe_audio(np.zeros(16000))
        self.assertEqual(result, "")
