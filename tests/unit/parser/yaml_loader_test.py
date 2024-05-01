from lark import Tree, Token

from ryon.parser.yaml_loader import yaml_to_ast


def test_yaml_to_tree():
    yaml_data = """
    !Tree
    subtree:
      - !Token "STRING hello"
    node: greeting
    """
    result = yaml_to_ast(yaml_data)
    assert isinstance(result, Tree)
    assert result.data == "greeting"
    assert isinstance(result.children[0], Token)
    assert result.children[0].type == "STRING"
    assert result.children[0].value == "hello"
