import os

import torch
import torchaudio
import pygame

def speak(path):
    pygame.init()
    current_directory = os.path.dirname(os.path.abspath(__file__))
    audio_file_path = os.path.join(current_directory, "output", path + ".wav")
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    pygame.quit()


def say(phrase:str):
    language = 'ru'
    model_id = 'v3_1_ru'
    sample_rate = 48000
    speaker = 'xenia'  #   'aidar', 'baya', 'kseniya', 'xenia', 'random'
    device = torch.device('cpu')

    # Загрузка модели
    model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                              model='silero_tts',
                              language=language,
                              speaker=model_id)
    model.to(device)

    # Генерация аудио
    audio = model.apply_tts(text=phrase,
                            speaker=speaker,
                            sample_rate=sample_rate)

    # Сохранение в файл
    torchaudio.save('output.wav', audio.unsqueeze(0), sample_rate)

    print("Аудио сохранено в 'output.wav'")







