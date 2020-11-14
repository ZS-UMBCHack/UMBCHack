from __future__ import annotations
from typing import List

from wiktionaryparser import WiktionaryParser


def parse(word: str, language: str) -> List[Word]:
    parser = WiktionaryParser()
    word_info = parser.fetch(word, language)
    word_origins: List[Word] = []

    for origin in word_info:
        pass
    return word_origins


class Word:
    def __init__(self, word: str, language: str, meanings: Meaning):
        self.word: str = word
        self.language: str = language
        self.etymons: List[Word] = []


class Meaning:
    def __init__(self):
        pass
