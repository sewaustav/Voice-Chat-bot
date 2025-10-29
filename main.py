import time

import vosk

from src.commands.commands import Execute, normalize
from src.commands.command_list import command_list
from src.voice.recognize import Recognition
from src.voice.tokeniztion import tokenization
from src.voice.wake_up import detect
from src.voice.speak import speak, say
from src.voice.answers.voice_response import *
from src.voice.answers.say_phrase import say_response

model_path = "./vosk-model-small-ru-0.22"
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

            if phrase.lower() == "стоп":
                say("Не уходи, еблан")
                speak()
                time.sleep(2)
                break

            # Обработка команды
            print("Команда:", phrase)
            tokens = tokenization(phrase)
            cmd = Execute(tokens)
            command = cmd.recognize_command()
            if command:
                if cmd.execute(command) == 1:
                    say(say_response(default_phrases=voice_success))
                    speak()
                else:
                    say(say_response(default_phrases=voice_no_recognized))
                    speak()
            else:
                say(say_response(default_phrases=voice_no_recognized))
                speak()

        else:
            a = detect()
            if a:
                say(say_response(default_phrases=voice_hello))
                speak()
                flag = True

if __name__ == "__main__":
    main()
