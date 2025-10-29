# 🎙️ Voice-Chat-bot  
**Голосовой ассистент на базе Picovoice + Vosk**  


> **Внимание!** Проект **работает только на Linux** (из-за специфики аудио-обработки и зависимостей).  
> Windows/macOS — пока не поддерживаются. 

---

## 🛠️ Stack & Technologies
<div align="center">

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Vosk-FF6F61?style=for-the-badge&logo=speechling&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/Picovoice-6C5CE7?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDJDNy4wMiAyIDIgNy4wMiAyIDEyczUuMDIgMTAgMTAgMTAgMTAtNS4wMiAxMC0xMFMxNi45OCAyIDEyIDJ6bTAgMThjLTQuNDEgMC04LTMuNTktOC04czMuNTktOCA4LTggOCAzLjU5IDggOC0zLjU5IDgtOCA4LTgtOC0zLjU5LTgtOHptLTQgN2wtMy41LTMuNUwxMiA4LjVsMy41IDMuNUwxOSA4bC0zLjUgMy41TDE5IDE1bC0zLjUtMy41TDExIDE1bC0zLjUtMy41TDE5IDhsLTMuNS0zLjV6IiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==&logoColor=white" />
  
</div>

---

## 🚀 Установка (Linux only)

### 1. Клонируем репозиторий

```bash

git clone https://github.com/sewaustav/Voice-Chat-bot.git bedolaga
cd bedolaga
```


### 2. Создаём виртуальное окружение (рекомендуется uv, но можно и venv)
#### Вариант A: Через uv (быстро и красиво)
```bash

# Проверяем, установлен ли pipx
pipx --version || {
  python -m pip install --user pipx
  python -m pipx ensurepath
}

# Устанавливаем uv
pipx install uv

# Создаём окружение на Python 3.11
uv venv --python 3.11

# Активируем
source .venv/bin/activate

# Устанавливаем зависимости
uv pip install -r requirements.txt
```
#### Вариант B: Классический venv
```bash

python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Настраиваем Picovoice Porcupine (Wake Word)

Перейдите на https://console.picovoice.ai
Создайте бесплатный аккаунт
Выберите Porcupine Wake Word
Придумайте фразу (доступен только английский язык)
Скачайте архив с моделью

```bash

# Распаковываем модель
unzip your-downloaded-model.zip -d WakeWordModel
```

### 4. Настраиваем конфигурацию
#### Вариант 1: Через .env (рекомендуется)
```bash

touch .env
```
Добавьте в .env:
```env

PICOKELVIN=ваш_access_key_из_picovoice
PICPATH=название_модели.ppn
```
#### Вариант 2: Прямо в config.py (если лень с .env)
Откройте config.py и замените:
```python
import os

from dotenv import load_dotenv

load_dotenv()

PICOVOICETOKEN = os.getenv('PICOKELVIN')
PICPATH = os.getenv('PICPATH')
```
на:
```python
PICOKELVIN = "ваш_access_key"
PICPATH = "WakeWordModel/название_модели.ppn"
```
### 5. Запускаем бота!
```bash

python main.py
```

Скажите вашу wake-фразу — и бот проснётся!
Список команд находится в src/commands/command_list.py


## 🔮 Что будет в следующей версии?

Интеграция с ChatGPT / DeepSeek / Llama 3 (локально)






