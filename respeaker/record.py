import io
import logging
import time
import requests
from threading import Thread, Event
import wave
from respeaker import Microphone
from respeaker.player import Player


SERVER_IP_PORT = 'http://192.168.3.126:8000/'

def task(quit_event):
    mic = Microphone(quit_event=quit_event)
    player = Player()
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

                        with wave.open(buffer, 'rb') as wav_file:
                            sample_rate = wav_file.getframerate()
                            n_channels = wav_file.getnchannels()
                            samp_width = wav_file.getsampwidth()

                        print(sample_rate)
                        player._play(response.content, sample_rate, n_channels, samp_width, False)
                    else:
                        logging.debug('Server response: %s' % response.text)
                except Exception as e:
                    logging.debug('Error sending to server: %s' % str(e))
            else:
                logging.debug('No data captured')

def main():
    logging.basicConfig(level=logging.DEBUG, force=True)

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
