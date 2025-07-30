import random


def say_response(phrase: str | None = None, default_phrases: list | None = None)->str:
    if phrase is not None:
        return phrase
    else:
        random.shuffle(default_phrases)
        return default_phrases[0]