# audio_server.py
import socket
import sounddevice as sd
import numpy as np

HOST = 'localhost'
PORT = 50007
SAMPLERATE = 16000
CHANNELS = 1
CHUNK = 1024  # bytes, not samples

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("Waiting for connection...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")

    with conn:
        with sd.OutputStream(samplerate=SAMPLERATE, channels=CHANNELS, dtype='int16') as stream:
            while True:
                data = conn.recv(CHUNK)
                if not data:
                    break
                samples = np.frombuffer(data, dtype='int16')
                stream.write(samples)
