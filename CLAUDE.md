# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Description
Development of a Catalan-language voice assistant utilizing a distributed architecture across two devices.

**Hardware & Software Constraints:**
- **ReSpeaker Core 1.0:** Handles recording and Wake Word Detection (WWD). Runs **Python 2.7.9**.
- **Raspberry Pi 4 (4GB):** Handles main processing and logic. Runs **Python 3.13**.
- **Connectivity:** Both devices communicate over the same local Wi-Fi network.

## Architecture
The system is designed to offload heavy processing from the input device:
1. **Capture (ReSpeaker):** Continuous audio monitoring for a wake word.
2. **Trigger:** Upon detection, the ReSpeaker records the subsequent command.
3. **Relay:** The audio is transmitted to the Raspberry Pi.
4. **Processing (Raspberry Pi):** A server on the Pi receives the audio, handles Speech-to-Text (STT), and processes the intent.

## Development Setup
To develop the ReSpeaker-side logic, install the custom library:
```bash
cd respeaker/respeaker_python_library
pip install .
```
**Dependencies:** `pocketsphinx`, `pyaudio`, `webrtcvad`, `requests`.

## Common Commands
- **Run Examples:**
  - Examples are located in `respeaker/respeaker_python_library/examples/`.
  - To run an example: `python3 respeaker/respeaker_python_library/examples/[filename].py`

## Project Structure
- `respeaker/`: Contains the custom library for ReSpeaker interaction and associated scripts.
- `raspberry/`: Reserved for the Raspberry Pi server and logic implementation.
