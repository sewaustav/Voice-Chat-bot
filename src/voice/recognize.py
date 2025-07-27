import json
from typing import Optional
import time

import vosk
import sounddevice as sd
import queue


# Очередь для аудиоданных
class Recognition:

    def __init__(self):
        self.audio_queue = queue.Queue()

    def audio_callback(self, indata, frames, time, status):
        """Колбек для записи аудио."""
        self.audio_queue.put(bytes(indata))

    # Настройка аудиопотока
    device_info = sd.query_devices(None, 'input')
    sample_rate = int(device_info['default_samplerate'])

    def recognize(self, model) -> Optional[str]:
        with sd.RawInputStream(
                samplerate=44100,
                blocksize=0,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
        ):
            recognizer = vosk.KaldiRecognizer(model, 44100)
            start = time.time()

            while True:

                if time.time() - start > 30:
                    return None

                data = self.audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result_json = json.loads(recognizer.Result())
                    text = result_json.get("text", "").strip()
                    if text:
                        return text
