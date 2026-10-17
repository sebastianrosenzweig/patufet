# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Description
Develop the software for a voice assistant designed for interaction in Catalan.

**Hardware:**
- **Processor:** Raspberry Pi 4 (4GB) - Primary logic and processing (running Python 3.13).
- **Input:** ReSpeaker Core 1.0 - Dedicated for recording and wake word detection (running Python 2.7.9).

Both devices are connected to the same wifi network.

## Architecture
The ReSpeaker continuously records audio and checks for the wake word. Once the wake word is detected, the ReSpeaker device records the voice command and sends the audio to the Raspberry Pi. The Raspberry Pi runs a server that receives the audio and does the voice processing.

## Steps
We first develop the software for the ReSpeaker, then the software for the Raspberry Pi.

## Rules
- No audio is allowed to leave the local network.
- Always plan first and ask in case of doubts before you execute.
- Create git commits with meaningful commit messages for authorized changes by me.
