import time
import pvporcupine
from pvrecorder import PvRecorder
import keyboard
from benchmark import Benchmark

def listen():
    porcupine = pvporcupine.create(
        access_key='6NS3SVHq+6QmUDwszyEk7hp+w+DriueAJz12GqxKriaWNbrRm4TMsw==',
        # keywords=['picovoice', 'bumblebee', 'aloha mora'],
        keyword_paths=["./HeyStone/Hey-stone_en_windows_v2_2_0.ppn"])

    recorder = PvRecorder(device_index=0, frame_length=porcupine.frame_length)
    recorder.start()
    print('Using device: %s' % recorder.selected_device)

    bench = Benchmark()


    while True:
        bench.start()
        pcm = recorder.read()
        keyword_index = porcupine.process(pcm)
        end_time = bench.end()

        if keyword_index == 0:
            print("Hi")

    porcupine.delete()