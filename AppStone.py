import flet as ft
import os
import subprocess
import webbrowser
import asyncio
import vosk
import sys
import sounddevice as sd
import queue
import pvporcupine
from pvrecorder import PvRecorder
from benchmark import Benchmark
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import Levenshtein
import pyautogui
import time
import pyperclip
from random import *
import json
import openai
import string
import config
import pyttsx3
from pyowm import OWM
import win32gui
import win32con
import keyboard
# from silero_voice import say
from playsound import playsound
import os
import pygame
from pynput.keyboard import Key, Controller

role = "Прими роль собеседника, по имени Александр. Ты разбирашься в программировании, дизайне, в компьютерных играх. на вопросы отчечаешь лаконично и коротко. не отвечаешь на вопросы связанные с политикой или религией."

result_queue = asyncio.Queue()

rus_abs = {
    "й": "q",
    "ц": "w",
    "у": "e",
    "к": "r",
    "е": "t",
    "н": "y",
    "г": "u",
    "ш": "i",
    "щ": "o",
    "з": "p",
    "х": "[",
    "ъ": "]",
    "ф": "a",
    "ы": "s",
    "в": "d",
    "а": "f",
    "п": "g",
    "р": "h",
    "о": "j",
    "л": "k",
    "д": "l",
    "ж": ";",
    "э": "'",
    "я": "z",
    "ч": "x",
    "с": "c",
    "м": "v",
    "и": "b",
    "т": "n",
    "ь": "m",
    "б": ",",
    "ю": ".",
    ",": "Shift+/",
    ".": "/",
    " ": " ",
    "ё": "`"

}

try:
    with open("commands.json", "r") as file:
        com = json.load(file)

except:
    com = {}

try:
    with open("sites.json", "r") as file:
        sites = json.load(file)
except:
    sites = {}

array = []

sysComands = ["гугл", "языка", "код", "текст", "почта", "погода", "линкедин", "ищи", "вкладка", "ютуб", "блокнот", "звук максимум", "звук минимум", "громче", "тише", "вк", "чат", "раскладка", "другое окно", "отмена", "диспетчер задач", "копировать", "вставить", "выделить", "вырезать", "сохранить", "клавиатура", "подтвердить", "режим печати", "режим кода", "строка", "горячие клавиши"]

cast_sites = []
for key in sites.keys():
    cast_sites.append(key)

cast_com = []
for key in com.keys():
    cast_com.append(key)

castComands = cast_com + cast_sites

Comands = sysComands + castComands

type_typing = 1

model = vosk.Model("smallmodel")
samlerate = 16000
device = 1
q = queue.Queue()

porcupine = pvporcupine.create(
    access_key=config.PICTOKEN,
    keyword_paths=["./HeyStone/Hey-stone_en_windows_v2_2_0.ppn"]
)

keyb = Controller()

weather_flag = False
start_detection = False
text_start_button = "Начать"

def main(page: ft.Page):
    page.title = "Бедолага - голосовой ассистент"
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False
    page.scroll = "AUTO"

    def speak(path):
        pygame.init()
        current_directory = os.path.dirname(os.path.abspath(__file__))
        audio_file_path = os.path.join(current_directory, "voice", path+".wav")
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        pygame.quit()



    def recognize_command(audio_text, commands_list):
        min_distance = float('inf')
        recognized_command = None

        for command in commands_list:
            distance = Levenshtein.distance(audio_text, command)
            if distance < min_distance:
                min_distance = distance
                recognized_command = command

        threshold_distance = 15

        if min_distance <= threshold_distance:
            return recognized_command
        else:
            return "Команда не распознана"

    def weatherFunc(temp, rain):
        if temp >= 15 and temp < 20 and rain == {}:
            print('В твоём городе сейчас достаточно тепло, но лучше надеть штаны и кофту')
            return 1
        elif temp >= 15 and temp < 20 and rain != {}:
            print('Судя по погоде, лучше надень штаны и кофту. И не забудь зонт, сейчас же дождь!')
            return 2
        elif temp > 7 and temp < 15 and rain == {}:
            print('Сейчас достаточно холодно, лучше надень куртку')
            return 3
        elif temp > 7 and temp < 15 and rain != {}:
            print('Сейчас достаточно холодно, лучше надень куртку. И не забудь зонт, сейчас же дождь!')
            return 4
        elif temp >= 0 and temp <= 7 and rain == {}:
            print('Сейчас холодно, надень тёплую куртку')
            return 5
        elif temp >= 0 and temp <= 7 and rain != {}:
            print('Сейчас холодно, надень тёплую куртку. И не забудь зонт, сейчас же дождь!')
            return 6
        elif temp < 0:
            print('Сейчас очень холодно, надень пуховик или теплую куртку')
            return 7
        elif temp >= 20:
            print('Сейчас жарко, надень шорты с футболкой')
            return 8

    def close_active_window():
        hwnd = win32gui.GetForegroundWindow()

        if hwnd != 0:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            return True
        else:
            return False

    def close_browser_tab():
        keyboard.press("ctrl")
        keyboard.press("w")
        time.sleep(1)
        keyboard.release("w")
        keyboard.release("ctrl")

    def press_enter():
        keyboard.press("enter")
        keyboard.release("enter")

    def change_lang():
        keyboard.press("shift")
        keyboard.press("alt")
        keyboard.release("shift")
        keyboard.release("alt")

    def change_win():
        keyboard.press("alt")
        keyboard.press("tab")
        keyboard.release("alt")
        keyboard.release("tab")

    def cansel_action():
        keyboard.press("ctrl")
        keyboard.press("z")
        keyboard.release("ctrl")
        keyboard.release("z")

    def task_manager():
        keyboard.press("ctrl")
        keyboard.press("alt")
        keyboard.press("del")
        keyboard.release("ctrl")
        keyboard.release("alt")
        keyboard.release("del")

    def copy_a():
        keyboard.press("ctrl")
        keyboard.press("c")
        keyboard.release("ctrl")
        keyboard.release("c")

    def paste_a():
        keyboard.press("ctrl")
        keyboard.press("v")
        keyboard.release("ctrl")
        keyboard.release("v")

    def select_all():
        keyboard.press("ctrl")
        keyboard.press("a")
        keyboard.release("ctrl")
        keyboard.release("a")

    def cut_o():
        keyboard.press("ctrl")
        keyboard.press("x")
        keyboard.release("ctrl")
        keyboard.release("x")

    def save_a():
        keyboard.press("ctrl")
        keyboard.press("s")
        keyboard.release("ctrl")
        keyboard.release("s")

    def press_enter():
        keyboard.press("enter")
        keyboard.release("enter")

    def press_tab():
        keyboard.press("tab")
        keyboard.press("tab")

    def change_keyboard():
        global type_typing
        if type_typing < 2:
            type_typing +=1
        else: type_typing = 0

    def print_text_anywhere(word):
        print(type_typing)
        keyboard.write(word)
        # for char in word:
        #     if type_typing == 0:
        #         keyb.press(rus_abs[char])
        #         keyb.release(rus_abs[char])
        #
        #     elif type_typing == 1:
        #         keyboard.press(rus_abs[char])
        #     else:
        #         pyautogui.write(rus_abs[char])

    def print_text_eng(word):
        for char in word:
            keyb.press(char)
            keyb.release(char)

    def GptAnswer(array):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "\n".join(array)}
                ],
                max_tokens=200,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
        except Exception as err:
            print("[INFO]: Error: " + err)

        reply = response.choices[0].message.content
        array.append(reply)

        return reply

    def changeVolume(percent):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        currentVolumeScalar = volume.GetMasterVolumeLevelScalar()
        targetVolumeScalar = currentVolumeScalar + (percent / 100.0)
        volume.SetMasterVolumeLevelScalar(targetVolumeScalar, None)

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)

        q.put(bytes(indata))

    activeDetection = False

    def main_func(weather_flag):
        with sd.RawInputStream(
                samplerate=samlerate,
                blocksize=8000,
                device=device,
                dtype='int16',
                channels=1,
                callback=callback) as stream:

            history = []

            rec = vosk.KaldiRecognizer(model, samlerate)
            pr_m = False
            search = False
            code = False
            hot_key = False
            count = 1
            empty_count = 0
            try:
                with open("commands.json", "r") as file:
                    com = json.load(file)

            except: com = {}

            try:
                with open("sites.json", "r") as file:
                    sites = json.load(file)
            except: sites = {}
            print("[INFO] Говорите...")
            global activeDetection
            activeDetection = True
            while activeDetection:
                data = q.get()
                if rec.AcceptWaveform(data):
                    print(" ")
                    print(count)
                    result = rec.Result()
                    i = 14
                    message = ""
                    while True:
                        try:
                            if result[i] == '"':  # define end of phrase
                                break
                            message += result[i]
                            i += 1
                        except Exception as _ex:

                            print(_ex)
                            break
                    print(message)
                    mes = ft.Container(
                        content = ft.Text(f"{message}", color="white", weight=ft.FontWeight.W_300, width=150),
                        bgcolor="#00B9FB",
                        border_radius=ft.border_radius.all(15),
                        padding=ft.padding.all(10)
                    )
                    if message != "":
                        page.add(
                            mes
                        )
                    if message != "":
                        empty_count = 0
                        predicted_category = recognize_command(message, Comands)
                        if "спящий режим" in message or "выключись" in message:
                            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                        elif "выключи систему" in message:
                            os.system("shutdown /s /t 1")
                        elif "выключи браузер" in message or "закрой браузер" in message:
                            process_name = "chrome.exe"
                            os.system(f"taskkill /f /im {process_name}")

                        if predicted_category not in sysComands:

                            for key, value in com.items():
                                if key in message:
                                    try:
                                        subprocess.Popen(value)
                                        print(key)
                                        answ = ft.Container(
                                            content=ft.Text(f"{key}", color="white", weight=ft.FontWeight.W_300,
                                                            width=150),
                                            bgcolor="#FF2052",
                                            border_radius=ft.border_radius.all(15),
                                            padding=ft.padding.all(10)
                                        )
                                        page.add(
                                            answ
                                        )
                                    except: pass

                            for key, value in sites.items():
                                if key in message:
                                    try:
                                        webbrowser.open(value)
                                        print(key)
                                        answ = ft.Container(
                                            content=ft.Text(f"{key}", color="white", weight=ft.FontWeight.W_300,
                                                            width=150),
                                            bgcolor="#FF2052",
                                            border_radius=ft.border_radius.all(15),
                                            padding=ft.padding.all(10)
                                        )
                                        page.add(
                                            answ
                                        )
                                    except: pass



                        if weather_flag:
                            try:
                                city = message
                                owm = OWM('a99a76ecfd5f4739737d50a7f8604843')
                                mgr = owm.weather_manager()
                                observation = mgr.weather_at_place(city)
                                w = observation.weather
                                t = w.temperature('celsius')['temp']
                                r = w.rain
                                o = ""
                                if r == {}:
                                    o = "Сейчас дождя нет"

                                res = weatherFunc(t, r)
                                t = round(t)
                                answ = ft.Container(
                                    content=ft.Text(f"{t}, {o}, {res}", color="white", weight=ft.FontWeight.W_300,
                                                    width=150),
                                    bgcolor="#FF2052",
                                    border_radius=ft.border_radius.all(15),
                                    padding=ft.padding.all(10)
                                )
                                page.add(
                                    answ
                                )
                                if o != "":
                                    speak("pogoda9")
                                else: speak("seichas")
                                if int(t) < 0:
                                    speak("minus")
                                speak(str(t))
                                speak("pogoda"+str(res))
                            except:
                                pass
                            finally:
                                weather_flag = False

                        elif "написал" in message or "закончил писать" in message:
                            pr_m = False
                            code = False
                            speak("pechatoff")
                            answ = ft.Container(
                                content=ft.Text("Отключил режим печати", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )
                            print("Done typing")

                        elif predicted_category == "горячие клавиши" and (code or pr_m):
                            hot_key = True
                            print("HOOOOOOt")

                        elif ("закрой" in message or "заверши" in message) and ("программу" in message or "приложение" in message):
                            resu = close_active_window()
                            print(resu)
                            resu = close_active_window()
                            print(resu)
                            ann = ["budetispolneno", "est", "slushaus", "seichas", "zakrivau"]
                            shuffle(ann)
                            speak(ann[0])
                            answ = ft.Container(
                                content=ft.Text(f"закрываю программу", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )


                        elif predicted_category == "раскладка" and ((not code and not pr_m) or hot_key):
                            change_lang()

                        elif predicted_category == "другое окно" and ((not code and not pr_m) or hot_key):
                            change_win()
                            print("другое окно")
                            hot_key = False

                        elif predicted_category == "отмена" and ((not code and not pr_m) or hot_key):
                            print("отмена")
                            cansel_action()
                            hot_key = False

                        elif predicted_category == "диспетчер задач" and ((not code and not pr_m) or hot_key):
                            print("диспетчер задач")
                            task_manager()
                            hot_key = False

                        elif predicted_category == "копировать" and ((not code and not pr_m) or hot_key):
                            print("копировать")
                            copy_a()
                            hot_key = False

                        elif predicted_category == "вставить" and ((not code and not pr_m) or hot_key):
                            print("вставить")
                            paste_a()
                            hot_key = False

                        elif predicted_category == "выделить" and ((not code and not pr_m) or hot_key):
                            print("выделить")
                            select_all()
                            hot_key = False

                        elif predicted_category == "вырезать" and ((not code and not pr_m) or hot_key):
                            print("вырезать")
                            cut_o()
                            hot_key = False

                        elif predicted_category == "сохранить" and ((not code and not pr_m) or hot_key):
                            print("сохранить")
                            save_a()
                            hot_key = False

                        elif predicted_category == "подтвердить" or predicted_category == "строка" and ((not code and not pr_m) or hot_key):
                            print("enter")
                            press_enter()
                            hot_key = False

                        elif predicted_category == "клавиатура" and ((not code and not pr_m) or hot_key):
                            print(type_typing)
                            change_keyboard()
                            hot_key = False



                        elif pr_m:

                            printMessage = message
                            printMessage = printMessage.replace(" точка", ". ")
                            printMessage = printMessage.replace(" запятая", ", ")
                            printMessage = printMessage.replace("точка", ". ")
                            printMessage = printMessage.replace("запятая", ", ")
                            print_text_anywhere(printMessage)

                            answ = ft.Container(
                                content=ft.Text("написал", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )
                            time.sleep(5)
                            speak("napisal")

                        elif code:
                            # open sublime text or notepad
                            text_to_code = message
                            text_to_code = text_to_code.replace("если", "if")
                            text_to_code = text_to_code.replace("пока", "while")
                            text_to_code = text_to_code.replace("для", "for")
                            text_to_code = text_to_code.replace("функция ", "def function_")
                            text_to_code = text_to_code.replace("от", "(")
                            text_to_code = text_to_code.replace("параметр ", "param_")
                            text_to_code = text_to_code.replace("процедура", "def proc_")
                            text_to_code = text_to_code.replace("вернуть", "return")
                            text_to_code = text_to_code.replace("вывод", "print(")
                            text_to_code = text_to_code.replace("переменная ", "current_")
                            text_to_code = text_to_code.replace("один", "1")
                            text_to_code = text_to_code.replace("два", "2")
                            text_to_code = text_to_code.replace("три", "3")
                            text_to_code = text_to_code.replace("четыре", "4")
                            text_to_code = text_to_code.replace("пять", "5")
                            text_to_code = text_to_code.replace("шесть", "6")
                            text_to_code = text_to_code.replace("семь", "7")
                            text_to_code = text_to_code.replace("восемь", "8")
                            text_to_code = text_to_code.replace("девять", "9")
                            text_to_code = text_to_code.replace("ноль", "0")
                            # all numbers
                            text_to_code = text_to_code.replace("равно", "=")
                            text_to_code = text_to_code.replace("плюс", "+")
                            text_to_code = text_to_code.replace("минус", "-")
                            text_to_code = text_to_code.replace("разделить", "/")
                            text_to_code = text_to_code.replace("больше", ">")
                            text_to_code = text_to_code.replace("меньше", "<")
                            text_to_code = text_to_code.replace("запятая", ",")
                            text_to_code = text_to_code.replace("и", "and")
                            text_to_code = text_to_code.replace("или", "or")
                            text_to_code = text_to_code.replace("не", "not")

                            print(text_to_code)

                            if "while" in text_to_code or "for" in text_to_code or "if" in text_to_code:
                                text_to_code += ":"
                                print_text_eng(text_to_code)
                                press_enter()
                            elif "proc" in text_to_code:
                                text_to_code += "():"
                                print_text_eng(text_to_code)
                                press_enter()
                            elif "def" in text_to_code:
                                text_to_code += "):"
                                print_text_eng(text_to_code)
                                press_enter()
                            elif "print" in text_to_code:
                                text_to_code += ")"
                                print_text_eng(text_to_code)
                                press_enter()
                            else:
                                print_text_eng(text_to_code)
                                press_enter()

                            print(text_to_code)
                            text_to_code = ""
                            time.sleep(5)
                            speak("napisal")
                            answ = ft.Container(
                                content=ft.Text("написал", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )

                        elif search:
                            request_google = "https://www.google.com/search?q=" + message + "&num=10" + "&hl=ru"
                            webbrowser.open(request_google)
                            search = False
                            answ = ft.Container(
                                content=ft.Text(f"Ваш запрос {request_google}", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )

                        elif predicted_category == "текст" or predicted_category == "режим печати":
                            pr_m = True
                            print("text mode")
                            speak("texton")
                            answ = ft.Container(
                                content=ft.Text(f"режим печати активирован", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )

                        elif predicted_category == "код" or predicted_category == "режим кода":
                            speak("codeon")
                            print("code mode active")
                            answ = ft.Container(
                                content=ft.Text(f"режим кода активирован", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )
                            code = True

                        elif "пока бедолага" in message:
                            empty_count = 5





                        elif predicted_category == "выход":
                            ann = ["budetispolneno", "est", "slushaus", "seichas", "zakrivau"]
                            shuffle(ann)
                            speak(ann[0])
                            # time.sleep(0.5)
                            resu = close_active_window()
                            print(resu)
                            answ = ft.Container(
                                content=ft.Text(f"закрываю программу", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )



                        elif predicted_category == "ищи":
                            search = True
                            speak("islushau")
                            answ = ft.Container(
                                content=ft.Text(f"я вас слушаю, скажите запрос", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )

                        elif predicted_category == "вкладка":
                            ann = ["budetispolneno", "est", "slushaus", "seichas", "zakrivau"]
                            shuffle(ann)
                            speak(ann[0])
                            # time.sleep(0.5)
                            close_browser_tab()
                            answ = ft.Container(
                                content=ft.Text(f"режим печати активирован", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )

                        elif predicted_category == "гугл":
                            print("google")
                            ann = ["budetispolneno", "est", "slushaus", "seichas", "otkrivau"]
                            shuffle(ann)
                            speak(ann[0])
                            # time.sleep(0.5)
                            webbrowser.open("https://www.google.com")
                            answ = ft.Container(
                                content=ft.Text("открываю гугл...", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )


                        elif predicted_category == "ютуб":
                            ann = ["budetispolneno", "est", "slushaus", "seichas", "otkrivau"]
                            shuffle(ann)
                            speak(ann[0])
                            # time.sleep(0.5)
                            webbrowser.open("https://www.youtube.com/")
                            print("you tube")
                            answ = ft.Container(
                                content=ft.Text("открываю ...", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )

                        elif predicted_category == "почта":
                            print("inbox")
                            ann = ["budetispolneno", "est", "slushaus", "seichas", "otkrivau"]
                            shuffle(ann)
                            speak(ann[0])
                            # time.sleep(0.5)
                            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
                            answ = ft.Container(
                                content=ft.Text("открываю ...", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )

                        elif predicted_category == "линкедин":
                            ann = ["budetispolneno", "est", "slushaus", "seichas", "otkrivau"]
                            shuffle(ann)
                            speak(ann[0])
                            # time.sleep(0.5)
                            webbrowser.open("https://www.linkedin.com")
                            print("LinkedIn")
                            answ = ft.Container(
                                content=ft.Text("открываю ...", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )

                        elif predicted_category == "блокнот":
                            ann = ["budetispolneno", "est", "slushaus", "seichas", "otkrivau"]
                            shuffle(ann)
                            speak(ann[0])
                            # time.sleep(0.5)
                            subprocess.Popen(['notepad.exe'])
                            print("notepad")
                            answ = ft.Container(
                                content=ft.Text("открываю ...", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )

                        elif predicted_category == "громче":
                            try:
                                changeVolume(10)
                                ann = ["budetispolneno", "est", "slushaus", "seichas"]
                                shuffle(ann)
                                speak(ann[0])
                            except:
                                try:
                                    changeVolume(5)
                                    ann = ["budetispolneno", "est", "slushaus", "seichas"]
                                    shuffle(ann)
                                    speak(ann[0])
                                except:
                                    print("звук на максимуме")

                        elif predicted_category == "тише":

                            try:
                                changeVolume(-10)
                                ann = ["budetispolneno", "est", "slushaus", "seichas"]
                                shuffle(ann)
                                speak(ann[0])
                            except:
                                try:
                                    changeVolume(-5)
                                    ann = ["budetispolneno", "est", "slushaus", "seichas"]
                                    shuffle(ann)
                                    speak(ann[0])
                                except:
                                    devices = AudioUtilities.GetSpeakers()
                                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                                    volume = cast(interface, POINTER(IAudioEndpointVolume))

                                    volume.SetMasterVolumeLevel(-64.0, None)


                        elif predicted_category == "звук максимум":

                            devices = AudioUtilities.GetSpeakers()
                            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                            volume = cast(interface, POINTER(IAudioEndpointVolume))

                            volume.SetMasterVolumeLevel(0.0, None)
                            ann = ["budetispolneno", "est", "slushaus", "seichas"]
                            shuffle(ann)
                            speak(ann[0])

                        elif predicted_category == "звук минимум":

                            devices = AudioUtilities.GetSpeakers()
                            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                            volume = cast(interface, POINTER(IAudioEndpointVolume))

                            volume.SetMasterVolumeLevel(-64.0, None)
                            ann = ["budetispolneno", "est", "slushaus", "seichas"]
                            shuffle(ann)
                            speak(ann[0])

                        elif predicted_category == "вк" or predicted_category == "языка":
                            webbrowser.open("https://vk.com/")
                            print("VK")
                            ann = ["budetispolneno", "est", "slushaus", "seichas", "otkrivau"]
                            shuffle(ann)
                            speak(ann[0])
                            answ = ft.Container(
                                content=ft.Text("открываю ...", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )

                        elif predicted_category == "погода":
                            weather_flag = True
                            speak("vkakom")
                            answ = ft.Container(
                                content=ft.Text(f"В каком городе?", color="white", weight=ft.FontWeight.W_300,
                                                width=150),
                                bgcolor="#FF2052",
                                border_radius=ft.border_radius.all(15),
                                padding=ft.padding.all(10)
                            )
                            page.add(
                                answ
                            )

                        elif "чат" == predicted_category and config.TOKEN != "":
                            GptAnswer(array)



                    elif message == "":
                        empty_count += 1
                        if empty_count > 5:
                            stream.close()
                            detected("w")
                            break
                    count += 1
                if empty_count > 5:
                    empty_count = 0
                    detected("w")
                    break
            else:
                stream.close()
    def detected(e):
        try:
            porcupine = pvporcupine.create(
                access_key=config.PICTOKEN,
                keyword_paths=["./HeyStone/Hey-stone_en_windows_v2_2_0.ppn"] # config.WWDMODELPATH
            )
            recorder = PvRecorder(device_index=0, frame_length=porcupine.frame_length)
            bench = Benchmark()
            recorder.start()
            print("[INFO] произнесите активционную фразу...")

            answ = ft.Container(
                content=ft.Text(f"произнесите активционную фразу...", color="white", weight=ft.FontWeight.W_300,
                                width=150),
                bgcolor="#FF2052",
                border_radius=ft.border_radius.all(15),
                padding=ft.padding.all(10)
            )
            page.add(
                answ
            )
            while True:
                bench.start()
                pcm = recorder.read()
                keyword_index = porcupine.process(pcm)
                end_time = bench.end()


                if keyword_index == 0:
                    print("Hi")
                    speak("ac" + str(randint(1, 7)))
                    answ = ft.Container(
                        content=ft.Text(f"расспознанно", color="white", weight=ft.FontWeight.W_300,
                                        width=150),
                        bgcolor="#FF2052",
                        border_radius=ft.border_radius.all(15),
                        padding=ft.padding.all(10)
                    )
                    page.add(
                        answ
                    )
                    recorder.stop()

                    main_func(False)
                    porcupine.delete()
        except Exception as err: print(err)

    def offdetect(e):
        global activeDetection
        go_home("w")
        activeDetection = False

    def go_chat(e):
        page.route = "/chat"
        page.clean()
        page.add(
            ft.AppBar(title=ft.Text("Чат"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.ElevatedButton("Стоп", on_click=offdetect)
        )
        detected("w")

    pathToFile = ft.TextField(label="путь до файла")
    nameOfFile = ft.TextField(label="ключевое слово")

    def saveData(e):
        if not pathToFile.value or not nameOfFile.value:
            pathToFile.error_text = "Please enter your name"
            page.update()
        else:
            path = pathToFile.value
            name = nameOfFile.value
            print(name, path)
            try:
                with open("commands.json", "r") as file:
                    dictCom = json.load(file)
                    dictCom[name] = path
                with open("commands.json", "w") as file:
                    json.dump(dictCom, file)
            except: pass


    def go_commands(e):
        page.route = "/commands"
        page.clean()
        page.add(
            ft.AppBar(title=ft.Text("Добавить программу"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Stack([
                pathToFile,
            ]),
            ft.Stack([
                nameOfFile
            ]),
            ft.Stack([
                ft.ElevatedButton("Сохранить!", on_click=saveData),
            ]),
            ft.Stack([
                ft.ElevatedButton("Сайты", top=200, left=137, bgcolor="#50C878", color="#FDF5E6", on_click=go_sites),
            ],
            height=250),
            ft.Stack([
                ft.ElevatedButton("Настройки", top=10, on_click=go_settings),
                ft.ElevatedButton("Домой", top=10, left=137, on_click=go_home),
                ft.ElevatedButton("Команды", top=10, left=245, on_click=go_commands),

            ])
        )
        page.update()

    pathToSite = ft.TextField(label="путь до сайта")
    nameOfSite = ft.TextField(label="ключевое слово")

    def savesite(e):
        if not pathToSite.value or not nameOfSite.value:
            pathToSite.error_text = "Please enter your name"
            print("Np")
            page.update()
        else:
            path = pathToSite.value
            name = nameOfSite.value
            print(name, path)
            try:
                with open("sites.json", "r") as file:
                    dictCom = json.load(file)
                    dictCom[name] = path
                with open("sites.json", "w") as file:
                    json.dump(dictCom, file)
            except:
                pass

    def go_sites(e):
        page.route = "/sites"
        page.clean()
        page.add(
            ft.AppBar(title=ft.Text("Добавить сайт"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Stack([
                pathToSite,
            ]),
            ft.Stack([
                nameOfSite
            ]),
            ft.Stack([
                ft.ElevatedButton("Сохранить!", on_click=savesite),
            ]),
            ft.Stack([
                ft.ElevatedButton("Приложения", top=200, left=115, bgcolor="#318CE7", color="#FDF5E6", on_click=go_commands),
            ],
                height=250),
            ft.Stack([
                ft.ElevatedButton("Настройки", top=10, on_click=go_settings),
                ft.ElevatedButton("Домой", top=10, left=137, on_click=go_home),
                ft.ElevatedButton("Команды", top=10, left=245, on_click=go_commands),

            ],
                width=400,
                height=600)
        )
        page.update()

    chatGPTtoken = ft.TextField(label="chat-GPT токен")
    pictoken = ft.TextField(label="Picovoice токен")

    def chatBtn(e):
        if not chatGPTtoken.value:
            chatGPTtoken.error_text = "Please enter your name"
            page.update()
        else:
            gpt = chatGPTtoken.value
            with open("config.py", "r+") as file:
                lines = file.readlines()
                if len(lines) >= 1:
                    newToken = "TOKEN='" + gpt + "'\n"
                    print(newToken, type(newToken))
                    lines[0] = newToken
                    file.seek(0)
                    file.writelines(lines)

    def picBtn(e):
        if not pictoken.value:
            pictoken.error_text = "Please enter your name"
        else:
            pic = pictoken.value
            with open("config.py", "r+") as file:
                lines = file.readlines()
                if len(lines) >= 1:
                    lines[1] = "PICTOKEN='"+pic+"'\n"
                    file.seek(0)
                    file.writelines(lines)

    def go_settings(e):
        page.route = "/settings"
        page.clean()
        page.add(
            ft.AppBar(title=ft.Text("Настройки"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Stack([
                chatGPTtoken,
            ],
            height=50),
            ft.ElevatedButton("Сохранить!", on_click=chatBtn),
            ft.Stack([
                pictoken,
                ft.ElevatedButton("Сохранить!", top=65, on_click=picBtn),
                ft.ElevatedButton("Настройки", top=342, on_click=go_settings),
                ft.ElevatedButton("Домой", top=342, left=137, on_click=go_home),
                ft.ElevatedButton("Команды", top=342, left=245, on_click=go_commands),

            ],
            height=500,
            width=500,
            )
        )
        page.update()


    def go_home(e):
        page.route = "/"
        page.clean()
        page.add(
            ft.AppBar(title=ft.Text("Главная"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Stack([
                ft.ElevatedButton("Старт", top=300, width=170, left=95, bgcolor="#0136A0", color="#FDF5E6", on_click=go_chat),
                # ft.ElevatedButton("Cтоп", top=350, width=170, left=95, bgcolor="#EB4C42", color="#FDF5E6", on_click=offdetect),
                ft.ElevatedButton("Настройки", top=444, on_click=go_settings),
                ft.ElevatedButton("Домой", top=444, left=137, on_click=go_home),
                ft.ElevatedButton("Команды", top=444, left=245, on_click=go_commands),

            ],
            width=400,
            height=600
            )
        )
        page.update()

    page.add(
        ft.AppBar(title=ft.Text("Главная"), bgcolor=ft.colors.SURFACE_VARIANT),
        ft.Stack([
            ft.ElevatedButton("Старт", top=300, width=170, left=95, bgcolor="#0136A0", color="#FDF5E6", on_click=go_chat),
            # ft.ElevatedButton("Cтоп", top=350, width=170, left=95, bgcolor="#EB4C42", color="#FDF5E6", on_click=offdetect),
            ft.ElevatedButton("Настройки", top=444, on_click=go_settings),
            ft.ElevatedButton("Домой", top=444, left=137, on_click=go_home),
            ft.ElevatedButton("Команды", top=444, left=245, on_click=go_commands),
        ],
        width=400,
        height=600
        )
    )




ft.app(target=main)