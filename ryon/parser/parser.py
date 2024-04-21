from lark import Lark, Tree
from lark.indenter import PythonIndenter
from pathlib import Path


class RyonParser:
    def __init__(self):
        self._parser = Lark.open(
            Path(__file__).parent / "main.lark", parser="lalr", postlex=PythonIndenter(), start="module"
        )

    def parse(self, data: str) -> Tree:
        return self._parser.parse(data)
