<h1>
  Patufet <img src="assets/patufet.png" alt="Patufet" width="25"> — A Tiny Catalan Voice Q&A System
</h1>

A lightweight, voice-based question-answering system in Catalan, powered by Retrieval-Augmented Generation (RAG) and designed to run on a Raspberry Pi.

Patufet lets you ask questions in Catalan using your voice and receive spoken answers in Catalan. The system combines open-source speech and translation models with Wikipedia retrieval and a locally running small language model (LLM), bringing voice-based AI to resource-constrained hardware. 
The system uses a client-server architecture, with a Raspberry Pi in the backend, while a client device captures audio, sends questions, and plays back the answers.

## Demo

Click the image for watching the demo! The demo uses a ReSpeaker Core 1.0 as the client device to interact with the Patufet backend. 
The wake word "Patufet" is recognized by the ReSpeaker using its on-board processing capabilities.

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

Follow the installation instructions in the dedicated READMEs for each component.

## Learnings & Future Research
* I could not find a model for Catalan speech transcription that runs sufficiently fast on a Raspberry Pi. Existing models like https://huggingface.co/projecte-aina/faster-whisper-large-v3-ca-3catparla or https://huggingface.co/BSC-LT/whisper-bsc-large-v3-cat are too big and slow. Future research could focus on developing Catalan models for edge use cases, e.g. by adapting tiny or base whisper models.  
* The translation and answering in English is unfortunately (still) necessary since Qwen or other small LLMs produce lots of errors when working with Catalan text. Future research could focus on adapting tiny LLMs for Catalan text input and output.
* Translation and speech synthesis in Catalan already work very well on a Raspberry Pi thanks to the great work of the Barcelona Supercomputing Center, the cooperative Col·lectivaT, Softcatalà, and the AINA project! :-) 

## License
MIT

## Visca!

