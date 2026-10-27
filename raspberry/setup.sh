#!/usr/bin/env bash
set -Eeuo pipefail

# Install eSpeak NG
if ! command -v espeak-ng >/dev/null 2>&1; then
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update
        sudo apt-get install -y espeak-ng
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y espeak-ng
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --needed --noconfirm espeak-ng
    else
        echo "Error: Unsupported package manager. Install espeak-ng manually." >&2
        exit 1
    fi
else
    echo "espeak-ng is already installed."
fi

# Check download utility
if ! command -v curl >/dev/null 2>&1; then
    echo "Error: curl is required. Please install curl." >&2
    exit 1
fi

# Create models directory relative to the current directory
mkdir -p ./models

BASE_URL="https://huggingface.co/rhasspy/piper-voices/resolve/main/ca/ca_ES/upc_ona/medium"

TTSMODEL="ca_ES-upc_ona-medium.onnx"
TTSCONFIG="ca_ES-upc_ona-medium.onnx.json"
LLMMODEL="tinyllama-1.1b-chat-v1.0-q4_k_m.gguf"

download_file() {
    local filename="$1"
    local url="$2"
    local destination="./models/$filename"
    local tmp="${destination}.part"

    if [[ -s "$destination" ]]; then
        echo "Already downloaded: $destination"
        return
    fi

    echo "Downloading $filename..."
    rm -f "$tmp"

    if curl --fail --location --retry 3 \
        --output "$tmp" "$url"; then
        mv "$tmp" "$destination"
        echo "Saved: $destination"
    else
        rm -f "$tmp"
        echo "Error downloading $filename" >&2
        return 1
    fi
}

download_file "$TTSMODEL" "$BASE_URL/$TTSMODEL?download=true"
download_file "$TTSCONFIG" "$BASE_URL/$TTSCONFIG?download=true"
download_file "$LLMMODEL" "https://huggingface.co/hieupt/TinyLlama-1.1B-Chat-v1.0-Q4_K_M-GGUF/resolve/main/$LLMMODEL?download=true"

echo
echo "Setup complete!"
echo "eSpeak NG: $(command -v espeak-ng)"
echo "TTS-Model:     ./models/$TTSMODEL"
echo "TTS-Config:    ./models/$TTSCONFIG"
echo "LLM-Model:    ./models/$LLMMODEL"
