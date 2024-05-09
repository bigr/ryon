from pathlib import Path

import pytest
from ryon.hlir.hlir import HLIRTransformer

from ryon.compiler import RyonCompiler
from ryon.parser import RyonParser


@pytest.fixture
def tests_data_dir():
    return Path(__file__).parent / "data"


@pytest.fixture
def parser():
    return RyonParser()


@pytest.fixture
def compiler():
    return RyonCompiler()


@pytest.fixture
def hlir_transformer():
    return HLIRTransformer()
