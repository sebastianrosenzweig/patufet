from pathlib import Path

import numpy as np
from piper import PiperVoice
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = Path("models/ca_ES-upc_pau-x_low.onnx")

voice = PiperVoice.load(str(model))
sample_rate = voice.config.sample_rate

def synthesize(text: str) -> tuple[np.ndarray, int]:
    """
    Synthesize speech locally.

    Returns:
        audio: mono int16 NumPy array
        sample_rate: audio sample rate in Hz
    """
    if not text.strip():
        return np.zeros(0, dtype=np.int16), sample_rate

    chunks = []

    for chunk in voice.synthesize(text):
        samples = np.frombuffer(
            chunk.audio_int16_bytes,
            dtype="<i2",
        )
        chunks.append(samples)

    if not chunks:
        return np.zeros(0, dtype=np.float32), sample_rate

    audio = np.concatenate(chunks).copy()
    audio_float = audio.astype(np.float32) / 32768.0

    return audio_float, sample_rate
