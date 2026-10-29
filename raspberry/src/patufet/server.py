import asyncio
import io
import logging
import wave

import numpy as np
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from .rag import generate_response
from .transcription import transcribe_audio
from .tts import synthesize

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Allow all origins for testing, but adjust as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def receive_audio(request: Request):
    # Get the raw body
    body = await request.body()

    if not body:
        return JSONResponse(content={"error": "No data received"}, status_code=400)

    # Convert to numpy array
    # The ReSpeaker provides 16000Hz, 16-bit (2 bytes), Mono (1 channel)
    audio_data = np.frombuffer(body, dtype=np.int16)
    audio_float = audio_data.astype(np.float32) / 32768.0
    audio_float = audio_float[
        int(0.25 * 16000):]  # truncate audio a bit to avoid bits of the wake word leaking into transcription

    # Trigger transcription
    text = await asyncio.to_thread(transcribe_audio, audio_float)
    if text:
        logger.info(f"Transcription finished: {text}")

        response = await asyncio.to_thread(generate_response, text)
        logger.info(f"Response: {response}")

        audio, sample_rate = synthesize(response)
        logger.info("Synthesis finished!")

        # Convert to int16 bytes
        audio_int16 = (audio * 32768.0).astype(np.int16)

        # Create WAV file in memory
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int16.tobytes())

        return Response(content=buffer.getvalue(), media_type="audio/wav")

    else:
        logger.info("Transcription produced no text.")

    # Return the success message
    return JSONResponse(content={"status": "command processed"})


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)
