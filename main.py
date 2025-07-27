import vosk

from src.voice.recognize import Recognition
from src.voice.wake_up import detect
from src.voice.speak import speak, say

model_path = "/home/sewa/Documents/Bedolaga/vosk-model-small-ru-0.22"
model = vosk.Model(model_path)

flag = False

if __name__ == "__main__":
    r = Recognition()
    while True:
        if flag:
            phrase = r.recognize(model)
            if phrase is None:
                flag = False
                continue  # Переход обратно к detect()

            # Обработка команды
            print("Команда:", phrase)
            if phrase.lower() == "стоп":
                break
        else:
            a = detect()
            if a: flag = True
