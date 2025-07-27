import os

import torch
import torchaudio
import pygame


def speak():
    pygame.init()
    # Получаем абсолютный путь к корню проекта (где находится main.py)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Строим путь к аудиофайлу относительно корня проекта
    audio_file_path = os.path.join(project_root, "voice", "output", "output.wav")

    pygame.mixer.init()
    try:
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
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
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Строим путь к директории output относительно корня проекта
    output_dir = os.path.join(project_root, "voice", "output")
    # Создаем директорию, если ее нет
    os.makedirs(output_dir, exist_ok=True)
    # Полный путь к файлу
    output_path = os.path.join(output_dir, "output.wav")
    torchaudio.save(output_path, audio.unsqueeze(0), sample_rate)

    print("Аудио сохранено в 'output.wav'")

# say("Я тут, готова выполнить любой приказ")
# speak()