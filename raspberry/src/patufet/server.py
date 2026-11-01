import asyncio
import io
import logging
import wave
import numpy as np
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from .rag import generate_response
from .transcription import transcribe_audio
from .tts import synthesize

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

async def process_audio_request(body: bytes) -> bytes | None:
    """
    Processes the raw audio data: transcribes, generates a response, and synthesizes speech.
    Returns the generated audio response if successful, else None.
    """
    if not body:
        return None

    # Convert to numpy array
    # The ReSpeaker provides 16000Hz, 16-bit (2 bytes), Mono (1 channel)
    audio_data = np.frombuffer(body, dtype=np.int16)
    audio_float = audio_data.astype(np.float32) / 32768.0

    # Truncate audio to avoid bits of the wake word leaking into transcription
    # 0.25 * 16000 = 4000 samples
    audio_float = audio_float[int(0.25 * 16000):]

    # Trigger transcription
    text = await asyncio.to_thread(transcribe_audio, audio_float)

    if not text:
        logger.info("Transcription produced no text.")
        return None

    logger.info(f"Transcription finished: {text}")

    # Generate response
    response_text = await asyncio.to_thread(generate_response, text)

    # Synthesize speech
    audio_out, sample_rate = synthesize(response_text)
    logger.info("Synthesis finished!")

    # Convert to int16 bytes
    audio_int16 = (audio_out * 32768.0).astype(np.int16)

    # Create WAV file in memory
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int16.tobytes())

    return buffer.getvalue()

@app.post("/")
async def receive_audio(request: Request):
    body = await request.body()

    if not body:
        return JSONResponse(content={"error": "No data received"}, status_code=400)

    audio_bytes = await process_audio_request(body)

    if audio_bytes:
        return Response(content=audio_bytes, media_type="audio/wav")
    else:
        return JSONResponse(content={"status": "command processed"})

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)
