import pytest

from ryon.parser.yaml_dumper import ast_to_yaml
from ryon.parser.yaml_loader import yaml_to_ast
from tests.data.code_fragments import fragments


@pytest.mark.parametrize("fragment", fragments)
def test_yaml(fragment, parser):
    expected_tree = parser.parse(fragment.code)
    yaml = ast_to_yaml(expected_tree)
    actual_tree = yaml_to_ast(yaml)
    assert expected_tree == actual_tree
