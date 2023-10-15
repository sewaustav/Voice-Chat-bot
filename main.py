import os
import subprocess
import webbrowser
import asyncio
import dataset
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
import cv2
import numpy as np
import pyautogui
import time
import pyperclip
from random import *
import json
import eel
import openai
import string
import config
import pyttsx3
from pyowm import OWM
import win32gui
import win32con
from pyowm.utils import config as cn
from pyowm.utils import timestamps
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from sklearn.preprocessing import LabelEncoder
import keyboard
from silero_voice import va_speak

va_speak("привет")

# voice init
engine = pyttsx3.init()
engine.setProperty('rate',200)
engine.setProperty('volume',0.9)
voice = engine.getProperty('voice')
engine.setProperty(voice, "!v/m1")

# create a role
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

array = []

def close_active_window():
    hwnd = win32gui.GetForegroundWindow()

    if hwnd != 0:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        return True
    else:
        return False

def close_browser_tab():
    pyperclip.copy(word)
    keyboard.press("ctrl")
    keyboard.press("w")
    time.sleep(1)
    keyboard.release("w")
    keyboard.release("ctrl")

def press_enter():
    keyboard.press("enter")
    keyboard.release("enter")

def press_tab():
    keyboard.press("tab")
    keyboard.press("tab")

def print_text_anywhere(word):
    for char in word:
        pyautogui.write(rus_abs[char])

def print_text_eng(word):
    for char in word:
        pyautogui.write(char)



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


model = vosk.Model("smallmodel")
samlerate = 16000
device = 1
q = queue.Queue()

def weatherFunc(temp, rain):
    if temp >= 15 and temp < 20 and rain == {}:
        return 'В твоём городе сейчас достаточно тепло, но лучше надеть штаны и кофту'
    elif temp >= 15 and temp < 20 and rain != {}:
        return 'Судя по погоде, лучше надень штаны и кофту. И не забудь зонт, сейчас же дождь!'
    elif temp > 7 and temp < 15 and rain == {}:
        return 'Сейчас достаточно холодно, лучше надень куртку'
    elif temp > 7 and temp < 15 and rain != {}:
        return 'Сейчас достаточно холодно, лучше надень куртку. И не забудь зонт, сейчас же дождь!'
    elif temp >= 0 and temp <= 7 and rain == {}:
        return 'Сейчас холодно, надень тёплую куртку'
    elif temp >= 0 and temp <= 7 and rain != {}:
        return 'Сейчас холодно, надень тёплую куртку. И не забудь зонт, сейчас же дождь!'
    elif temp < 0:
        return 'Сейчас очень холодно, надень пуховик или теплую куртку'
    elif temp >= 20:
        return 'Сейчас жарко, надень шорты с футболкой'

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

porcupine = pvporcupine.create(
    access_key='6NS3SVHq+6QmUDwszyEk7hp+w+DriueAJz12GqxKriaWNbrRm4TMsw==',
    keyword_paths=["./HeyStone/Hey-stone_en_windows_v2_2_0.ppn"]
)



# Предварительно подготовленные данные для обучения
training_data = dataset.training_data

# Создание словаря слов
word_dict = {}
index = 1
for question, _ in training_data:
    words = question.lower().split()
    for word in words:
        if word not in word_dict:
            word_dict[word] = index
            index += 1

# Преобразование текстовых данных в числовой формат
training_input = []
training_output = []
for question, category in training_data:
    words = question.lower().split()
    vector = [word_dict[word] for word in words]
    training_input.append(vector)
    training_output.append(category)

# Преобразование меток в числовой формат
label_encoder = LabelEncoder()
training_output = label_encoder.fit_transform(training_output)

# Преобразование входных данных в одинаковую длину
max_sequence_length = max(len(seq) for seq in training_input)
training_input = tf.keras.preprocessing.sequence.pad_sequences(training_input, maxlen=max_sequence_length)

# Создание модели нейронной сети
my_model = Sequential()
my_model.add(Embedding(len(word_dict) + 1, 64, input_length=max_sequence_length))
my_model.add(LSTM(64))
my_model.add(Dense(64, activation='relu'))
my_model.add(Dense(len(label_encoder.classes_), activation='softmax'))

# Компиляция и обучение модели
my_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
my_model.fit(training_input, training_output, epochs=100, verbose=0)


weather_flag = False


def main(weather_flag):
    with sd.RawInputStream(
            samplerate=samlerate,
            blocksize=8000,
            device=device,
            dtype='int16',
            channels=1,
            callback=callback) as stream:

        rec = vosk.KaldiRecognizer(model, samlerate)
        pr_m = False
        search = False
        code = False
        count = 1
        empty_count = 0
        print( "[INFO] Говорите..." )
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                print(" ")
                print(count)
                result = rec.Result()
                i = 14
                message = ""
                while True:
                    try:
                        if result[i] == '"': # define end of phrase
                            break
                        message += result[i]
                        i+=1
                    except Exception as _ex:

                        print(_ex)
                        break
                print(message)
                if message != "":
                    empty_count = 0
                    question = message
                    words = question.lower().split()
                    vector = [word_dict.get(word, 0) for word in words]  # Используем 0 для неизвестных слов
                    input_data = tf.keras.preprocessing.sequence.pad_sequences([vector], maxlen=max_sequence_length)
                    predicted_probabilities = my_model.predict(input_data)[0]
                    predicted_category_index = tf.argmax(predicted_probabilities)
                    predicted_category = label_encoder.classes_[predicted_category_index]
                    print(predicted_category)
                    # await result_queue.put(predicted_category)
                    if "спящий режим" in message or "выключись" in message:
                        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    elif "выключи систему" in message:
                        os.system("shutdown /s /t 1")
                    elif "выключи браузер" in message or "закрой браузер"in message:
                        process_name = "chrome.exe"
                        os.system(f"taskkill /f /im {process_name}")

                    if weather_flag:
                        try:
                            city = message
                            owm = OWM('a99a76ecfd5f4739737d50a7f8604843')
                            mgr = owm.weather_manager()
                            observation = mgr.weather_at_place(city)
                            w = observation.weather
                            t = w.temperature('celsius') ['temp']
                            r = w.rain
                            o = ""
                            if r == {}:
                                o = "Сейчас дождя нет"

                            res = weatherFunc(t, r)
                            print(res, t, o)
                        except: pass
                        finally:
                            weather_flag = False

                    elif "напиши" in message:
                        pr_m = True

                    elif "написал" in message or "закончил писать" in message:
                        pr_m = False

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

                    elif "писать код" or "написать кот" or "написать скотт" in message:

                        print("code mode active")
                        code = True

                    elif "пока бедолага" in message:
                        stream.close()
                        break

                    elif pr_m:
                        printMessage = message
                        printMessage = printMessage.replace("напиши ", "")
                        printMessage = printMessage.replace(" точка", ". ")
                        printMessage = printMessage.replace(" запятая", ", ")
                        print_text_anywhere(printMessage)

                    elif predicted_category == "выход":
                        resu = close_active_window()
                        print(resu)

                    elif search:
                        request_google = "https://www.google.com/search?q=" + message + "&num=10" + "&hl=ru"
                        webbrowser.open(request_google)
                        search = False

                    elif predicted_category == "поиск":
                        search = True

                    elif predicted_category == "вкладка":
                        close_browser_tab()

                    elif predicted_category == "гугл":
                        webbrowser.open("https://www.google.com")
                        print("google")

                    elif predicted_category == "ютуб":
                        webbrowser.open("https://www.youtube.com/")
                        print("you tube")

                    elif predicted_category == "почта":
                        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
                        print("inbox")

                    elif predicted_category == "линкедин":
                        webbrowser.open("https://www.linkedin.com")
                        print("LinkedIn")

                    elif predicted_category == "блокнот":
                        subprocess.Popen(['notepad.exe'])
                        print("notepad")

                    elif predicted_category == "звук+":
                        try:
                            changeVolume(10)
                        except:
                            try:
                                changeVolume(5)
                            except:
                                print("звук на максимуме")

                    elif predicted_category == "звук-":

                        try:
                            changeVolume(-10)
                        except:
                            try:
                                changeVolume(-5)
                            except:
                                devices = AudioUtilities.GetSpeakers()
                                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                                volume = cast(interface, POINTER(IAudioEndpointVolume))

                                volume.SetMasterVolumeLevel(-64.0, None)


                    elif predicted_category == "звук++":

                        devices = AudioUtilities.GetSpeakers()
                        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                        volume = cast(interface, POINTER(IAudioEndpointVolume))

                        volume.SetMasterVolumeLevel(0.0, None)

                    elif predicted_category == "звук--":

                        devices = AudioUtilities.GetSpeakers()
                        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                        volume = cast(interface, POINTER(IAudioEndpointVolume))

                        volume.SetMasterVolumeLevel(-64.0, None)

                    elif predicted_category == "вк" or "вк" in message:
                        webbrowser.open("https://vk.com/")

                    elif predicted_category == "погода":
                        weather_flag = True

                    elif "чат жпт" == predicted_category and config.TOKEN != "":
                        GptAnswer(array)

                elif message == "":
                    empty_count+=1
                    if empty_count > 5:
                        stream.close()
                        detected()
                        break
                count += 1
            if empty_count > 5:
                empty_count = 0
                break



                # definition commands




def detected():
    recorder = PvRecorder(device_index=0, frame_length=porcupine.frame_length)
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
            recorder.stop()

            main(weather_flag)
            porcupine.delete()

if __name__ == "__main__":
    detected()
