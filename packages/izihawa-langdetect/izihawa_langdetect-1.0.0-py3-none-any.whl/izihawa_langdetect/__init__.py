import fire

from ._langdetect import detect_language


def run():
    fire.Fire(detect_language)
