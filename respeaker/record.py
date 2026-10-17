import logging
import time
import requests
from threading import Thread, Event

from respeaker import Microphone

SERVER_IP_PORT = 'http://192.168.3.126:8000/'

def task(quit_event):
    mic = Microphone(quit_event=quit_event)
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

                    if response.status_code == 200 and 'command processed' in response.text:
                        logging.debug('Server: Command processed')
                    else:
                        logging.debug('Server response: %s' % response.text)
                except Exception as e:
                    logging.debug('Error sending to server: %s' % str(e))
            else:
                logging.debug('No data captured')

def main():
    logging.basicConfig(level=logging.INFO)

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
