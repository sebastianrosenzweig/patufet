import numpy as np
from faster_whisper import WhisperModel

# Configuration for the transcription model
MODEL_SIZE = "base"  # "projecte-aina/faster-whisper-large-v3-ca-3catparla"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"

# Initialize the model
# We load it once globally to avoid the overhead of reloading on every request
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)


def transcribe_audio(source: np.ndarray) -> str:
    """
    Transcribes the audio source provided.
    Returns the transcribed text.
    """
    segments, _ = model.transcribe(source, beam_size=5, language="ca")
    return "".join([segment.text for segment in segments]).strip()
