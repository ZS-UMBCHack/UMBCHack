from __future__ import annotations
from typing import List
from enum import Enum
import re

from wiktionaryparser import WiktionaryParser

paren_quote_pattern = re.compile('\\("[^(]+"\\)')
quote_pattern = re.compile('\\([^(]+\\)')


def get_etymology_trees(word_str: str, language: str) -> List[Word]:
    parser = WiktionaryParser()
    word_info = parser.fetch(word_str, language)
    word_origins: List[Word] = []

    for origin in word_info:
        word = Word(word_str, language)
        parse(origin['etymology'])
    return word_origins


def parse(text: str):
    subbed_text: str = text
    quote_parens: List[str] = []
    parens: List[str] = []

    index = 0
    match = re.search(paren_quote_pattern, subbed_text)
    while match is not None:
        subbed_text = re.sub(paren_quote_pattern, '$q' + str(index), subbed_text, count=1)
        quote_parens.append(match.group())
        index += 1
        match = re.search(paren_quote_pattern, subbed_text)

    index = 0
    match = re.search(quote_pattern, subbed_text)
    while match is not None:
        subbed_text = re.sub(quote_pattern, '$p' + str(index), subbed_text, count=1)
        parens.append(match.group())
        index += 1
        match = re.search(quote_pattern, subbed_text)




class Word:
    def __init__(self, word: str, language: str):
        self.word: str = word
        self.language: str = language
        self.etymons: List[Word] = []


if __name__ == '__main__':
    get_etymology_trees("sound", "English")
