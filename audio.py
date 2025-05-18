import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

import os
import sys

sys.stderr = open(os.devnull, 'w')


def transcribe_from_mic_offline(model_path="vosk-model-small-en-us-0.15", duration=5, samplerate=16000):
    q = queue.Queue()

    def callback(indata, frames, time, status):
        # if status:
        #     print(f"Status: {status}")
        q.put(bytes(indata))

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, samplerate)

    # print(f"Listening for {duration} seconds... Speak now.")
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        for _ in range(int(samplerate / 8000 * duration)):
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                return result.get("text", "")
    
    # Final result if no full match during stream
    final_result = json.loads(recognizer.FinalResult())
    return final_result.get("text", "")

# print(transcribe_from_mic_offline())

if __name__ == "__main__":
    while True:
        print(transcribe_from_mic_offline())