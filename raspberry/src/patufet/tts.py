import logging

import numpy as np
from huggingface_hub import hf_hub_download
from piper import PiperVoice

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

repo_id = "rhasspy/piper-voices"
model_path = hf_hub_download(
    repo_id=repo_id,
    filename="ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx"
)
_ = hf_hub_download(
    repo_id=repo_id,
    filename="ca/ca_ES/upc_ona/medium/ca_ES-upc_ona-medium.onnx.json"
)

voice = PiperVoice.load(model_path)
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
