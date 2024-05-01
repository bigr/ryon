import yaml
from typing import Any
from lark import Tree, Token


class YAMLASTLoader(yaml.SafeLoader):
    """Custom YAML loader to deserialize Lark Tree and Token objects."""


def tree_constructor(loader: YAMLASTLoader, node: yaml.nodes.MappingNode) -> Tree:
    """
    Reconstruct a Lark Tree object from a YAML node.

    Args:
        loader (YAMLASTLoader): The YAML loader instance.
        node (yaml.nodes.MappingNode): The YAML node representing a Tree.

    Returns:
        Tree: The reconstructed Lark Tree object.
    """
    value: dict[str, Any] = loader.construct_mapping(node)
    children = value.get("subtree", [])
    rule = value["node"]
    return Tree(rule, children)


def token_constructor(loader: YAMLASTLoader, node: yaml.nodes.ScalarNode) -> Token:
    """
    Reconstruct a Lark Token object from a YAML node.

    Args:
        loader (YAMLASTLoader): The YAML loader instance.
        node (yaml.nodes.ScalarNode): The YAML node representing a Token.

    Returns:
        Token: The reconstructed Lark Token object.
    """
    value: str = loader.construct_scalar(node)
    typ, val = value.split(" ", 1)
    return Token(typ, val)


# Register custom constructors to the loader
YAMLASTLoader.add_constructor("!Tree", tree_constructor)
YAMLASTLoader.add_constructor("!Token", token_constructor)


def yaml_to_ast(yaml_data: str) -> Tree:
    """
    Deserialize YAML string back into a Lark parse tree.

    Args:
        yaml_data (str): YAML formatted string representing a Lark parse tree.

    Returns:
        Tree: The deserialized Lark parse tree.
    """
    return yaml.load(yaml_data, Loader=YAMLASTLoader)
