import time

import pyautogui
import subprocess

from src.commands.command_list import app_execute_list
from src.commands.hotkeys_config import HOT_KEYS


class BrowserCommand:
    @staticmethod
    def open_new_tab():
        pyautogui.hotkey('ctrl', 't')

    @staticmethod
    def open_new_window():
        pyautogui.hotkey('ctrl', 'n')

    @staticmethod
    def close_tab():
        pyautogui.hotkey('ctrl', 'w')

    @staticmethod
    def open_closed_tab():
        pyautogui.hotkey('ctrl', 'shift', 't')

    @staticmethod
    def next_tab():
        pyautogui.hotkey('ctrl', 'tab')

    @staticmethod
    def prev_tab():
        pyautogui.hotkey('ctrl', 'shift', 'tab')

class Browser(BrowserCommand):

    def __init__(self, commands:list):
        self.commands = commands

    def analyze(self)->int:
        if any(key in app_execute_list for key in self.commands):
            if "открыть" in self.commands:
                if "новое" in self.commands:
                    if "вкладка" in self.commands:
                        super().open_new_tab()
                        return 1
                    elif "окно" in self.commands:
                        super().open_new_window()
                        return 1
                elif "закрытый" in self.commands and "вкладка" in self.commands:
                    super().open_closed_tab()
                    return 1
                elif "следующий" in self.commands and "вкладка" in self.commands:
                    super().next_tab()
                    return 1
                elif "предыдущий" in self.commands and "вкладка" in self.commands:
                    super().prev_tab()
                    return 1
            elif "закрыть" in self.commands and "вкладка" in self.commands:
                super().close_tab()
                return 1
            else: return 0
        else: return 0


class SystemCommand:
    @staticmethod
    def open_program(program: str):
        subprocess.Popen([program])

    @staticmethod
    def close_program(program: str):
        subprocess.call(["pkill", "-f", program])

# --- Звук ---
class SoundCommand:
    @staticmethod
    def volume_up():
        subprocess.call(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"])

    @staticmethod
    def volume_down():
        subprocess.call(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"])

    @staticmethod
    def mute_toggle():
        subprocess.call(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"])

# --- Клавиатура ---
class KeyboardCommand:
    @staticmethod
    def press_enter():
        pyautogui.press('enter')

    @staticmethod
    def press_tab():
        pyautogui.press('tab')

    @staticmethod
    def type_text(text: str):
        pyautogui.write(text)

# --- Основной класс, анализирующий команды ---
class Assistant(SystemCommand, SoundCommand, KeyboardCommand):
    def __init__(self, commands: list):
        self.commands = [cmd.lower() for cmd in commands]

    def analyze(self)->int:
        if "открыть" in self.commands:
            for word in self.commands:
                if word not in {"открыть", "программу"}:
                    self.open_program(word)
                    return 1

        elif "закрыть" in self.commands:
            for word in self.commands:
                if word not in {"закрыть", "программу"}:
                    self.close_program(word)
                    return 1

        elif "звук" in self.commands:
            if "громче" in self.commands:
                self.volume_up()
                return 1
            elif "тише" in self.commands:
                self.volume_down()
                return 1
            elif "выключить" in self.commands or "включить" in self.commands:
                self.mute_toggle()
                return 1

        elif "громче" in self.commands:
            self.volume_up()
            return 1
        elif "тише" in self.commands:
            self.volume_down()
            return 1

        # need to remake
        elif "ввести" in self.commands:
            index = self.commands.index("ввести")
            if index + 1 < len(self.commands):
                self.type_text(self.commands[index + 1])
                return 1

        elif "enter" in self.commands:
            self.press_enter()
            return 1
        elif "tab" in self.commands:
            self.press_tab()
            return 1

        return 0


class HotKeyHandler:
    def __init__(self, commands: list):
        self.commands = [cmd.lower() for cmd in commands]
        self.last_keys = None

    def execute(self):

        if "отмена" in self.commands:
            return self.undo_last()

        for command in self.commands:
            if command in HOT_KEYS:
                keys = HOT_KEYS[command]

                if keys == ["custom"] and command == "базаданных":
                    self._launch_pgadmin_and_browser()
                    return 1
                else:
                    print("HHHHH")
                    self._press_keys(keys)
                    return 1
        return 0

    def undo_last(self):
        if self.last_keys:
            self._press_keys(self.last_keys)
            return 1
        else:
            print("Нет предыдущей комбинации для отмены.")
            return 0

    @staticmethod
    def _press_keys(keys: list):
        pyautogui.hotkey(*keys)

    @staticmethod
    def _launch_pgadmin_and_browser():
        subprocess.Popen(["pgadmin4"])
        time.sleep(3)
        subprocess.Popen(["chromium", "http://127.0.0.1:5050"])

