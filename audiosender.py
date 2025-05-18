# audio_client.py
import socket
import sounddevice as sd
import sys

target_address = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'

HOST = target_address  # Replace with the server's IP address
PORT = 50007
SAMPLERATE = 16000
CHANNELS = 1
CHUNK = 1024  # Match this with the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server, streaming audio...")

    def callback(indata, frames, time, status):
        if status:
            print(f"InputStream status: {status}")
        s.sendall(indata)

    with sd.InputStream(samplerate=SAMPLERATE, channels=CHANNELS, dtype='int16', callback=callback, blocksize=CHUNK):
        try:
            import time
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopped by user.")
