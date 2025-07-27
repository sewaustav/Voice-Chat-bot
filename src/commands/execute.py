import pyautogui
from src.commands.command_list import browser_list, app_execute_list


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

    def analyze(self):
        if any(key in app_execute_list for key in self.commands):
            if "открыть" in self.commands:
                if "новое" in self.commands:
                    if "вкладка" in self.commands:
                        super().open_new_tab()
                        return 1
                    elif "окно" in self.commands:
                        super().open_new_window()
                        return 1
                elif "закрытый" in self.commands:
                    super().open_closed_tab()
                    return 1
                elif "следующий" in self.commands:
                    super().next_tab()
                    return 1
                elif "предыдущий" in self.commands:
                    super().prev_tab()
                    return 1
            elif "закрыть" in self.commands:
                super().close_tab()
                return 1
            else: return 0
        else: return 0
