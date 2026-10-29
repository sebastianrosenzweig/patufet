# CLAUDE.md

This file provides guidance to Claude Code (`claude.ai/code`) when working with this repository.

## Project Overview

**Patufet** is a lightweight, Catalan-language, voice-based question-answering system powered by Retrieval-Augmented Generation (RAG).

The project uses a distributed client-server architecture consisting of two devices:

- **ReSpeaker Core 1.0:** Acts as the audio client. Handles audio capture, wake word detection (WWD), and communication with the backend.
- **Raspberry Pi 4 (4 GB RAM):** Acts as the backend server. Handles speech recognition, translation, Wikipedia retrieval, local LLM inference, and text-to-speech synthesis.

The goal is to provide a complete voice-based question-answering experience in Catalan while running the main AI processing pipeline locally on affordable hardware.

**Important considerations:**

- The ReSpeaker and Raspberry Pi have different Python environments.
- ReSpeaker-side code must remain compatible with Python 2.7.9.
- Raspberry Pi-side code must remain compatible with Python 3.13.
- Do not introduce dependencies that require a Python version unsupported by the target device.
- The two devices communicate over the same local Wi-Fi network.
- Keep client-side processing lightweight. Computationally expensive AI workloads belong on the Raspberry Pi.

## System Architecture

Patufet follows a client-server architecture in which the ReSpeaker handles audio interaction and the Raspberry Pi performs the main processing.

### 1. Client: ReSpeaker Core 1.0

The ReSpeaker is responsible for:

1. Continuously monitoring audio input for a predefined wake word.
2. Detecting the wake word using Wake Word Detection (WWD).
3. Recording the user's spoken question in Catalan.
4. Sending the recorded audio to the Raspberry Pi backend over the local network.
5. Receiving the generated audio response.
6. Playing the response through its audio output.

The ReSpeaker should primarily handle audio-related operations rather than AI inference.

### 2. Backend: Raspberry Pi 4

The Raspberry Pi runs a server that receives audio requests from the client and executes the following processing pipeline:

1. **Speech-to-Text (STT):** Transcribes the incoming Catalan audio into text using an open-source speech recognition model.
2. **Translation (Catalan → English):** Translates the transcription into English.
3. **Information Retrieval:** Uses the Wikipedia API to retrieve relevant English-language Wikipedia content based on the translated question.
4. **Answer Generation:** Uses a small locally running Large Language Model (LLM) to interpret the retrieved information and generate a concise answer in English.
5. **Translation (English → Catalan):** Translates the generated answer back into Catalan.
6. **Text-to-Speech (TTS):** Synthesizes the Catalan answer into audio using a Catalan speech synthesis model.
7. **Response:** Returns the synthesized audio to the ReSpeaker for playback.

The backend should perform all computationally intensive AI operations locally whenever possible. Audio is not allowed to leave the device.

## Repository Structure

The repository is organized around the two main devices:

```text
.
├── respeaker/
├── raspberry/
└── CLAUDE.md
```

### `respeaker/`

Contains the ReSpeaker client-side implementation, including:

- Custom Python library for ReSpeaker interaction.
- Wake word detection, recording and playback functionality.
- Scripts to set up the ReSpeaker

### `raspberry/`

Contains the Raspberry Pi backend implementation, including:

- Server-side logic.
- Audio request handling.
- Speech recognition and translation.
- Wikipedia retrieval and RAG pipeline.
- Local LLM integration.
- Catalan text-to-speech synthesis.

## Common Commands
Call `poetry run python -m pytest -s unittests/` from within the `raspberry/` directory to run the server-side unittests. 

