import pytest

from ryon.parser import RyonParser
from ryon.parser.yaml_dumper import ast_to_yaml
from tests.data.code_fragments import fragments, NumberCodeFragment


def test_parser_initialization():
    RyonParser()


@pytest.mark.parametrize("fragment", fragments)
def test_parser(parser, fragment):
    ast = parser.parse(fragment.code)
    actual = ast_to_yaml(ast)

    assert actual == fragment.ast, f"Failed parsing {fragment.name}: {fragment.code}"


@pytest.mark.parametrize(
    "number_type", ("I8", "I16", "I32", "I64", "I128", "U8", "U16", "U32", "U64", "U128", "F16", "F32", "F64")
)
def test_parser_basic_numbers(parser, number_type):
    fragment = NumberCodeFragment()
    ast = parser.parse(fragment.code(number_type))
    actual = ast_to_yaml(ast)

    assert actual == fragment.ast(number_type), f"Failed parsing {number_type}: {fragment.code}"
