import os
from faster_whisper import WhisperModel

# Configuration for the transcription model
MODEL_SIZE = "tiny" # "projecte-aina/faster-whisper-large-v3-ca-3catparla"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"

# Initialize the model
# We load it once globally to avoid the overhead of reloading on every request
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes the audio file provided in file_path.
    Returns the transcribed text.
    """
    segments, _ = model.transcribe(file_path, beam_size=5, language="ca")
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

    print(f"Saved transcription to {filepath}")
    return filepath
