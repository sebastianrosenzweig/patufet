<h1>
  Patufet <img src="assets/patufet.png" alt="Patufet" width="25"> — A Tiny Catalan Voice Q&A System
</h1>

This is a proof-of-concept for a lightweight, voice-based question-answering system in Catalan, powered by Retrieval-Augmented Generation (RAG) and designed to run on a Raspberry Pi.

Patufet lets you ask questions in Catalan using your voice and receive spoken answers in Catalan. The system combines open-source speech and translation models with Wikipedia retrieval and a locally running small language model (LLM). 
It uses a client-server architecture with a Raspberry Pi in the backend, while a client device captures audio, sends questions, and plays back the answers.

The system is designed to minimise external data sharing, as all voice processing and AI inference take place locally. 
The only exception is the Wikipedia RAG component, which sends a transcript of the user question to Wikipedia to retrieve relevant information. 
No audio recordings or full conversation history are shared.

Rather than delivering a ready-to-use product, the goal of this project is to explore the limits of existing small voice and language processing models for Catalan and point to challenges for future research (s. Section "Learnings" below).

[Find out who is Patufet here :-)](https://en.wikipedia.org/wiki/Patufet)

## Demo

Click the image for watching the demo! The demo uses a ReSpeaker Core 1.0 as the client device to interact with the Patufet backend. 
The wake word "Patufet" is recognized by the ReSpeaker using its on-board processing capabilities. Disclaimer: The processing of the request takes ca. 30 sec. - the video has been shortened for demo purposes.

<p>
  <a href="https://www.youtube.com/watch?v=vzMBKtugbCQ">
    <img src="https://img.youtube.com/vi/vzMBKtugbCQ/0.jpg"
         alt="Patufet demo"
         width="600">
  </a>
</p>

## Processing Pipeline

🎙️ **Audio input**:
A client device records a spoken question in Catalan and sends the audio to the Raspberry Pi over the network.

📝 **Speech recognition (model: whisper base)**: 
The server transcribes the incoming audio into text using an open-source speech recognition model.

🌍 **Translation to English (model: SalamandraTA-2B-instruct)**: 
The Catalan transcription is translated into English to support the English-language retrieval and answering pipeline.

🔎 **Wikipedia retrieval**: 
The translated question is used to retrieve relevant English Wikipedia content through the Wikipedia API.

🧠 **Answer generation (model: qwen2.5-0.5b-instruct-fp16)**: 
A small LLM running locally processes the retrieved content and generates a concise answer in English.

🔄 **Translation to Catalan (model: SalamandraTA-2B-instruct)**: 
The generated answer is translated back into Catalan.

🔊 **Speech synthesis (model: piper ca_ES-upc_ona-medium)**:
A Catalan text-to-speech model synthesizes the translated answer into audio, which is returned to the client for playback.

## Installation

Follow the installation instructions in the dedicated READMEs for each device.

## Learnings & Future Research
* Good news: Processing voice and language in Catalan on a Raspberry Pi is possible with SOTA models, thanks to the great work of the Barcelona Supercomputing Center, the cooperative Col·lectivaT, Softcatalà, and the AINA project! However, the processing is still too slow for a usable commercial product (s. bottlenecks below).
* I could not find a model for Catalan speech transcription that runs sufficiently fast on a Raspberry Pi. Existing models like https://huggingface.co/projecte-aina/faster-whisper-large-v3-ca-3catparla or https://huggingface.co/BSC-LT/whisper-bsc-large-v3-cat don't fit in memory and are too slow. Future research could focus on developing Catalan models for edge use cases, e.g. by adapting tiny or base whisper models. The currently used whisper base model makes many mistakes in Catalan but seems to offer the best compromise between transcription speed and quality at the moment. 
* The workaround to do RAG in English instead of Catalan is unfortunately (still) necessary since Qwen or other small LLMs produce lots of errors when working with Catalan text. Future research could focus on adapting tiny LLMs for Catalan text input and output to reduce errors.

## License
MIT

## Visca!

