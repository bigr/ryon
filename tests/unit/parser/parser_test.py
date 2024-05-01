import pytest

from ryon.parser import RyonParser
from ryon.parser.yaml_dumper import ast_to_yaml
from tests.data.code_fragments import fragments


def test_parser_initialization():
    RyonParser()


@pytest.mark.parametrize("fragment", fragments)
def test_parser(parser, fragment):
    ast = parser.parse(fragment.code)
    actual = ast_to_yaml(ast)

    assert actual == fragment.ast, f"Failed parsing {fragment.name}: {fragment.code}"
