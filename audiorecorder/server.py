#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import socket
import SocketServer
import BaseHTTPServer
import logging
import sys

import pyaudio
from respeaker.pixel_ring import pixel_ring

# --------------------------------------------------
# Configuration
# --------------------------------------------------
HOST = '0.0.0.0'
PORT = 8000
AUDIO_PATH = '/audio'

MAX_BUFFER_CHUNKS = 100

# --------------------------------------------------
# Shared audio buffer
# --------------------------------------------------
class AudioBuffer(object):
    def __init__(self):
        self.condition = threading.Condition()
        self.chunks = []
        self.sequence = 0

    def publish(self, data):
        if not data:
            return

        with self.condition:
            self.sequence += 1
            self.chunks.append((self.sequence, data))

            # Limit memory usage
            if len(self.chunks) > MAX_BUFFER_CHUNKS:
                self.chunks = self.chunks[-MAX_BUFFER_CHUNKS:]

            self.condition.notify_all()

    def get_after(self, sequence):
        with self.condition:
            while True:
                # Return only audio newer than the client's cursor
                available = [
                    (seq, data)
                    for seq, data in self.chunks
                    if seq > sequence
                ]

                if available:
                    return available

                self.condition.wait()

# Global buffer instance
audio_buffer = AudioBuffer()

# --------------------------------------------------
# Microphone capture
# --------------------------------------------------
def capture_audio(quit_event):
    logging.info('Starting audio capture with PyAudio')

    p = pyaudio.PyAudio()

    # Open a stream for recording
    # Defaulting to 16000Hz mono 16-bit
    stream = p.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=16000,
                     input=True,
                     frames_per_buffer=4096)

    while not quit_event.is_set():
        try:
            # Read raw bytes from the input stream
            data = stream.read(4096, exception_on_overflow=False)
            if data:
                audio_buffer.publish(data)
        except Exception as e:
            logging.exception('Audio capture error: %s', e)
            # Brief pause before retrying to avoid rapid log spamming
            quit_event.wait(1)

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()

# --------------------------------------------------
# HTTP handler
# --------------------------------------------------
class AudioHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != AUDIO_PATH:
            self.send_error(404, 'Use /audio')
            return

        self.send_response(200)
        self.send_header(
            'Content-Type',
            'application/octet-stream'
        )
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'close')
        self.end_headers()

        # Start with the newest available audio.
        # Old buffered audio is not replayed to new clients to ensure "live" feeling.
        with audio_buffer.condition:
            sequence = audio_buffer.sequence

        logging.info(
            'Audio client connected: %s',
            self.client_address
        )

        try:
            pixel_ring.set_color(rgb=0x00FF00)
            while True:
                chunks = audio_buffer.get_after(sequence)

                for seq, data in chunks:
                    # Skip data if this client fell behind the retained buffer.
                    with audio_buffer.condition:
                        oldest = (
                            audio_buffer.chunks[0][0]
                            if audio_buffer.chunks else seq
                        )

                    if seq < oldest:
                        sequence = oldest - 1
                        continue

                    self.wfile.write(data)
                    self.wfile.flush()
                    sequence = seq

        except (IOError, socket.error):
            # Normal when the client disconnects
            pixel_ring.set_color(rgb=0x400000)
            pass

        finally:
            pixel_ring.set_color(rgb=0x400000)
            logging.info(
                'Audio client disconnected: %s',
                self.client_address
            )


    def log_message(self, fmt, *args):
        logging.info(
            '%s - %s',
            self.client_address[0],
            fmt % args
        )

# --------------------------------------------------
# Threaded HTTP server
# --------------------------------------------------
class ThreadedHTTPServer(
        SocketServer.ThreadingMixIn,
        BaseHTTPServer.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s'
    )

    pixel_ring.set_color(rgb=0x400000)

    quit_event = threading.Event()

    # Start audio capture in a separate thread
    capture_thread = threading.Thread(
        target=capture_audio,
        args=(quit_event,)
    )
    capture_thread.daemon = True
    capture_thread.start()

    try:
        server = ThreadedHTTPServer(
            (HOST, PORT),
            AudioHandler
        )
    except socket.error:
        logging.exception(
            'Could not bind to port %d. '
            'Is another server using it?',
            PORT
        )
        quit_event.set()
        return

    logging.info(
        'Audio server listening on http://%s:%d%s',
        HOST,
        PORT,
        AUDIO_PATH
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info('Shutting down')
    finally:
        quit_event.set()
        server.shutdown()
        server.server_close()

if __name__ == '__main__':
    main()
