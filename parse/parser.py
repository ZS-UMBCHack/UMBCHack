from wiktionaryparser import WiktionaryParser


class Parser:
    def __init__(self, word: str, language: str):
        parser = WiktionaryParser()
        self.word_info = parser.fetch(word)


class OriginTree:
    class Node:
        def __init__(self, language: str, word: str, etymons: List[Node]):
            self.language: str = language
            self.word: str = word
            self.etymons: List[Node] = etymons

    def __init__(self, root: Node):
        self.root: Node = root
