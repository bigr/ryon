from lark import Tree, Token

# Import the functions from your module
from ryon.parser.yaml_dumper import ast_to_yaml


def test_tree_to_yaml():
    token = Token("STRING", "hello")
    tree = Tree("greeting", [token])

    output = ast_to_yaml(tree)

    expected_output = "!Tree\n" "node: greeting\n" "subtree:\n" "- !Token 'STRING hello'\n"

    assert output == expected_output, "YAML output does not match expected"
