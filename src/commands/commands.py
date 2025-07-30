import Levenshtein
import pymorphy2

from src.commands.command_list import command_list as commands_keywords, hot_keys_list
from src.commands.command_list import app_list, browser_list, system_list, app_execute_list
from src.commands.execute import Browser, HotKeyHandler, Assistant

morph = pymorphy2.MorphAnalyzer()
def normalize(word):
    return morph.parse(word)[0].normal_form


class Execute:

    def __init__(self, phrase:list):
        self.phrase = phrase
        self.command_list = set()

    def recognize_command(self)->set:
        commands = set()
        for word in self.phrase:
            audio_text = normalize(word.lower())

            best_match = None
            best_score = 0

            for command, keywords in commands_keywords.items():
                for keyword in keywords:
                    score = Levenshtein.ratio(audio_text, keyword)
                    if score > best_score:
                        best_score = score
                        best_match = command

            if best_score > 0.7:
                commands.add(best_match)
                self.command_list.add(best_match)
            else: print("команда не распознана")
        return commands

    def execute(self, command)->str:
        commands = list(self.command_list)
        if len(commands) == 0:
            return "команда не распознана"
        print(commands)


        # recognize topic of task
        if any(x in commands for x in ["окно", "вкладка"]):
            br = Browser(commands)
            if br.analyze() == 1:
                return "Исполнено"
            else: return "Команда не распознана"

        elif any(x in commands for x in app_list.keys()) or "звук" in commands:
            a = Assistant(commands)
            if a.analyze() == 1:
                return "Исполнено"
            else: return "Команда не распознана"

        elif any(x in hot_keys_list for x in commands):
            hk = HotKeyHandler(commands)
            if hk.execute() == 1:
                return "Исполнено"
            else: return "Команда не распознана"

        # always last elif
        elif any(x in commands for x in ["закрой", "закрытый"]):
            hk = HotKeyHandler(commands)
            if hk.execute() == 1:
                return "Исполнено"
            else: return "Команда не распознана"


        else:
            print("Nothing")
            return "Команда не распознана"
