import vosk

from src.commands.commands import Execute, normalize
from src.commands.command_list import command_list
from src.voice.recognize import Recognition
from src.voice.tokeniztion import tokenization
from src.voice.wake_up import detect
from src.voice.speak import speak, say

model_path = "/home/sewa/Documents/Bedolaga/vosk-model-small-ru-0.22"
model = vosk.Model(model_path)

def main():
    flag = False
    r = Recognition()
    while True:
        if flag:
            phrase = r.recognize(model)
            if phrase is None:
                flag = False
                continue  # Переход обратно к detect()

            # Обработка команды
            print("Команда:", phrase)
            tokens = tokenization(phrase)
            cmd = Execute(tokens)
            command = cmd.recognize_command()
            if command:
                ph = cmd.execute(command)
                say(ph)
                speak()
            if phrase.lower() == "стоп":
                break
        else:
            a = detect()
            if a: flag = True

if __name__ == "__main__":
    main()
