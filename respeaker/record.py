import io
import logging
import pyaudio
import subprocess
import time
import requests
from threading import Thread, Event
import wave
from respeaker import Microphone


SERVER_IP_PORT = 'http://192.168.3.126:8000/'
loglevel = logging.DEBUG

def task(quit_event):
    logging.getLogger().setLevel(loglevel)
    logging.info("Starting thread...")

    while True:
        try:
            mic = Microphone(quit_event=quit_event)
            break
        except:
            time.sleep(1)
    logging.info("Start recording...")

    while not quit_event.is_set():
        if mic.wakeup('patufet'):
            logging.debug('Wake up')
            data = mic.listen()
            audio_bytes = ''.join(data)
            if data:
                logging.debug('Recording captured, sending to server...')
                try:
                    # Send the audio data to the Raspberry Pi
                    response = requests.post(
                        SERVER_IP_PORT,
                        data=audio_bytes,
                        headers={'Content-Type': 'application/octet-stream'}
                    )

                    if response.status_code == 200:
                        logging.debug('Server: Command processed')
                        buffer = io.BytesIO(response.content)
                        wav_file = wave.open(buffer, 'rb')

                        p = pyaudio.PyAudio()
                        stream = None

                        try:
                            sample_rate = wav_file.getframerate()
                            n_channels = wav_file.getnchannels()
                            samp_width = wav_file.getsampwidth()

                            stream = p.open(
                                format=p.get_format_from_width(samp_width),
                                channels=n_channels,
                                rate=sample_rate,
                                output=True
                            )

                            # Hack: Play silence before and after for response to be fully played back
                            if samp_width == 1:
                                silence = b'\x80' * (sample_rate * n_channels * samp_width)
                            else:
                                silence = b'\x00' * (sample_rate * n_channels * samp_width)

                            # Read and play audio in chunks
                            chunk_size = 1024
                            data = wav_file.readframes(chunk_size)

                            stream.write(silence)
                            while data:
                                stream.write(data)
                                data = wav_file.readframes(chunk_size)

                            stream.write(silence)

                        finally:
                            if stream is not None:
                                stream.stop_stream()
                                stream.close()

                            p.terminate()
                            wav_file.close()
                            buffer.close()
                    else:
                        logging.debug('Server response: %s' % response.text)
                except Exception as e:
                    logging.debug('Error sending to server: %s' % str(e))
            else:
                logging.debug('No data captured')

def main():
    logging.basicConfig(level=loglevel)

    quit_event = Event()
    thread = Thread(target=task, args=(quit_event,))
    thread.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            logging.debug('Quit')
            quit_event.set()
            break
    thread.join()

if __name__ == '__main__':
    main()
