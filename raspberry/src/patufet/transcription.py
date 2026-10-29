import logging
import os

import numpy as np
from faster_whisper import WhisperModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration for the transcription model
MODEL_SIZE = "base"  # "projecte-aina/faster-whisper-large-v3-ca-3catparla"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"

# Initialize the model
# We load it once globally to avoid the overhead of reloading on every request
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)


def transcribe_audio(source: str | np.ndarray) -> str:
    """
    Transcribes the audio source provided.
    Returns the transcribed text.
    """
    segments, _ = model.transcribe(source, beam_size=5, language="ca")
    return "".join([segment.text for segment in segments]).strip()


def save_transcription(text: str, file_path: str):
    """
    Saves the transcribed text to a file.
    The file name is the timestamp in UTC.
    """
    if not text:
        return

    # Ensure the data directory exists
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    filepath = os.path.join(data_dir, "tmp.txt")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    logger.info(f"Saved transcription to {filepath}")
    return filepath
