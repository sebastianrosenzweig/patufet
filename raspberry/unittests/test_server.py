import unittest

import os
import wave

import pytest
from fastapi.testclient import TestClient
from patufet.server import app

client = TestClient(app)

class TestServer(unittest.TestCase):
    def test_receive_audio_endpoint(self) -> None:
        """Test the POST / endpoint with a valid dummy wav file."""

        filepath = "test_received.wav"

        with wave.open(filepath, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(16000)
            wav_file.writeframes(b'\x00\x00' * 100)

        response = client.post("/", content=open(filepath, 'rb').read())

        assert response.status_code == 200
        assert response.json() == {"status": "command processed"}

        # Cleanup
        if os.path.exists(filepath):
            os.remove(filepath)

    def test_receive_audio_no_data(self) -> None:
        """Test the POST / endpoint with no data."""
        response = client.post("/", content=b"")
        assert response.status_code == 400
        assert "error" in response.json()
