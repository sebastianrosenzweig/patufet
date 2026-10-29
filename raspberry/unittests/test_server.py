import os
import wave
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from patufet.server import app

client = TestClient(app)

def test_receive_audio_endpoint():
    """Test the POST / endpoint with a valid dummy wav file."""

    filepath = "test_received.wav"

    with wave.open(filepath, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        wav_file.writeframes(b'\x00\x00' * 100)

    # Mock transcription to avoid real processing
    with patch('server.transcribe_audio') as mock_transcribe:
        mock_transcribe.return_value = "mocked transcription"

        response = client.post("/", content=open(filepath, 'rb').read())

        assert response.status_code == 200
        assert response.json() == {"status": "command processed"}

    # Cleanup
    if os.path.exists(filepath):
        os.remove(filepath)

def test_receive_audio_no_data():
    """Test the POST / endpoint with no data."""
    response = client.post("/", content=b"")
    assert response.status_code == 400
    assert "error" in response.json()
