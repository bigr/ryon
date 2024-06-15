from pathlib import Path

import pytest
from ryon.hlir.hlir import HLIRTransformer

from ryon.compiler import RyonCompiler
from ryon.parser import RyonParser
from ryon.symbols.symbols import RyonSymbolizer, SymbolTable


@pytest.fixture
def tests_data_dir():
    return Path(__file__).parent / "data"


@pytest.fixture
def parser():
    return RyonParser()


@pytest.fixture
def symbol_table():
    return SymbolTable()


@pytest.fixture
def symbolizer(symbol_table):
    return RyonSymbolizer(symbol_table)


@pytest.fixture
def compiler():
    return RyonCompiler()


@pytest.fixture
def hlir_transformer():
    return HLIRTransformer()
