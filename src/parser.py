from __future__ import annotations
from typing import List
import re

from wiktionaryparser import WiktionaryParser

quote_pattern = re.compile('\\([^(]+\\)')
delims = ' ;,.:\n'

origin_phrases = [
    'ultimately from',
    'from a variant of',
    'from earlier',
    'from',
    'abbreviation of',
    'borrowed from',
    'alteration of',
]
skip_phrases = [
    'variant of',
    'variants of',
    'equivalent to',
]
stop_phrases = [
    '\n'
]

segment_pattern = re.compile('|'.join(
    [f'({phrase})' for phrase in origin_phrases + skip_phrases + stop_phrases]
), re.IGNORECASE)


def get_etymology_trees(word_str: str, language: str) -> List[Word]:
    parser = WiktionaryParser()
    word_info = parser.fetch(word_str, language)
    word_origins: List[Word] = []

    for origin in word_info:
        word = Word(word_str, language)
        parse(origin['etymology'])
    return word_origins


def parse(text: str):
    text = re.sub(quote_pattern, '', text)
    segments = []

    start = None
    for match in re.finditer(segment_pattern, text):
        if start is not None:
            segments.append(remove_trailing_delim(text[start:match.start()].strip()))
        start = match.end()

    print(segments)


def remove_trailing_delim(text: str):
    while text[-1] in delims:
        text = text[0:-1]
    return text


class Word:
    def __init__(self, word: str, language: str):
        self.word: str = word
        self.language: str = language
        self.etymons: List[Word] = []


if __name__ == '__main__':
    get_etymology_trees("sound", "English")
