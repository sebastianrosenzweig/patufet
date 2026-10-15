import time
import urllib.request
import wave

SERVER_URL = 'http://192.168.3.124:8000/audio'
OUTPUT_FILE = 'recording.wav'

DURATION_SECONDS = 10
SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16-bit PCM = 2 bytes per sample


def main():
    bytes_to_capture = (
        DURATION_SECONDS * SAMPLE_RATE * CHANNELS * SAMPLE_WIDTH
    )

    captured = 0

    request = urllib.request.urlopen(SERVER_URL, timeout=15)

    try:
        with wave.open(OUTPUT_FILE, 'wb') as wav_file:
            wav_file.setnchannels(CHANNELS)
            wav_file.setsampwidth(SAMPLE_WIDTH)
            wav_file.setframerate(SAMPLE_RATE)

            while captured < bytes_to_capture:
                chunk = request.read(
                    min(4096, bytes_to_capture - captured)
                )
                print(chunk)

                if not chunk:
                    break

                wav_file.writeframesraw(chunk)
                captured += len(chunk)
    finally:
        request.close()

    print('Saved %s (%d bytes of audio)' % (OUTPUT_FILE, captured))


if __name__ == '__main__':
    main()