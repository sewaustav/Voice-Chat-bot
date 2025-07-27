import pvporcupine
from pvrecorder import PvRecorder

import config
from benchmark import Benchmark


def detect():
    try:

        porcupine = pvporcupine.create(
            access_key=config.PICOVOICETOKEN,
            keyword_paths=["./HeyStone/Hey-Stone_en_linux_v3_0_0.ppn"]
        )
        recorder = PvRecorder(device_index=1, frame_length=porcupine.frame_length)
        bench = Benchmark()
        recorder.start()
        print("[INFO] произнесите активционную фразу...")


        while True:
            bench.start()
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)
            end_time = bench.end()

            if keyword_index == 0:
                print("Hi")
                # speak("ac" + str(randint(1, 7)))

                recorder.stop()


                porcupine.delete()
                return 1
    except Exception as e:
        print(e)

