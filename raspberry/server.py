from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import datetime
import os
import wave

app = FastAPI()

# Allow all origins for testing, but adjust as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the data directory exists
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.post("/")
async def receive_audio(request: Request):
    # Get the raw body
    body = await request.body()

    if not body:
        return JSONResponse(content={"error": "No data received"}, status_code=400)

    # Generate filename with UTC timestamp
    now = datetime.datetime.utcnow()
    filename = f"{now.strftime('%Y%m%d_%H%M%S_%f')[:23]}.wav"
    filepath = os.path.join(DATA_DIR, filename)

    # Save the data as a valid WAV file
    # The ReSpeaker provides 16000Hz, 16-bit (2 bytes), Mono (1 channel)
    with wave.open(filepath, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 2 bytes for 16-bit
        wav_file.setframerate(16000)
        wav_file.writeframes(body)

    print(f"Saved audio to {filepath}")

    # Return the success message
    return JSONResponse(content={"status": "command processed"})

if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
